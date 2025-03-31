import logging
from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Any, Dict, List, Tuple, Set, Optional

class UnusedVarAnalysis(BaseAnalysis):
    def __init__(self, debug=True, **kwargs) -> None:
        super().__init__(**kwargs)
        # 数据结构用于跟踪变量操作
        self.write_ops = {}
        self.read_ops = set()
        self.unused_vars = {}
        self.debug = debug

        # 清除任何现有的日志处理器
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # 创建根日志记录器
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG if debug else logging.INFO)  # 设置为DEBUG级别

        # 主日志文件 - 只记录INFO级别及以上
        main_handler = logging.FileHandler('unused_vars.log', mode='w')
        main_handler.setLevel(logging.INFO)
        main_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(main_handler)

        # 调试日志文件 - 记录所有级别
        if debug:
            debug_handler = logging.FileHandler('unused_vars_debug.log', mode='w')
            debug_handler.setLevel(logging.DEBUG)  # 设置为DEBUG级别
            debug_handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(debug_handler)

            # 验证调试模式已启用
            logging.debug("调试模式已启用 - 这条消息应该出现在调试日志中")

        # 确保立即刷新
        for handler in logger.handlers:
            handler.flush()

    def log(self, message):
        """记录重要信息"""
        logging.info(message)
        for handler in logging.root.handlers:
            handler.flush()

    def debug_log(self, message):
        """记录调试信息"""
        if self.debug:
            # 直接使用logging.debug而不是logging.info
            logging.debug(f"DEBUG: {message}")
            for handler in logging.root.handlers:
                handler.flush()

    def write(self, dyn_ast: str, iid: int, old_vals: List[Any], new_val: Any) -> Any:
        """写操作钩子"""
        try:
            var_name = f"var_at_iid_{iid}"

            # 使用debug_log记录调试信息
            self.debug_log(f"Write operation at IID {iid} with value {new_val}")

            if var_name in self.write_ops and var_name not in self.read_ops:
                prev_iid, prev_val = self.write_ops[var_name]
                self.unused_vars[var_name] = (prev_iid, prev_val)
                message = f"UNUSED VARIABLE: {var_name} was written at IID {prev_iid} with value {prev_val} but never read before being written again at IID {iid}"
                self.log(message)

            self.write_ops[var_name] = (iid, new_val)

            if var_name in self.read_ops:
                self.read_ops.remove(var_name)
                self.debug_log(f"Removed {var_name} from read_ops")

        except Exception as e:
            self.log(f"Error in write hook: {e}")

        return new_val

    def read(self, dyn_ast: str, iid: int, val: Any) -> Any:
        """读操作钩子"""
        try:
            var_name = f"var_at_iid_{iid}"

            self.debug_log(f"Read operation at IID {iid} with value {val}")

            for name, (write_iid, write_val) in list(self.write_ops.items()):
                if str(write_val) == str(val):
                    self.read_ops.add(name)
                    self.debug_log(f"Marked variable {name} as read at IID {iid}")

        except Exception as e:
            self.log(f"Error in read hook: {e}")

        return val

    def read_identifier(self, dyn_ast: str, iid: int, val: Any) -> Any:
        """读取标识符的钩子"""
        self.debug_log(f"Read identifier at IID {iid} with value {val}")
        return self.read(dyn_ast, iid, val)

    def read_attribute(self, dyn_ast: str, iid: int, base: Any, name: str, val: Any) -> Any:
        """读取属性的钩子"""
        self.debug_log(f"Read attribute at IID {iid}: {base}.{name} = {val}")
        return self.read(dyn_ast, iid, val)

    def read_subscript(self, dyn_ast: str, iid: int, base: Any, sl: List, val: Any) -> Any:
        """读取下标的钩子"""
        self.debug_log(f"Read subscript at IID {iid}: {base}[{sl}] = {val}")
        return self.read(dyn_ast, iid, val)

    def memory_access(self, dyn_ast: str, iid: int, val: Any) -> Any:
        """内存访问钩子"""
        self.debug_log(f"Memory access at IID {iid} with value {val}")
        return val

    def end_execution(self) -> None:
        """分析完成时的最终处理"""
        self.log("===== Analysis Complete =====")

        # 检查程序结束时仍未被读取的变量
        never_used_vars = {}
        for var_name, (iid, val) in self.write_ops.items():
            if var_name not in self.read_ops:
                never_used_vars[var_name] = (iid, val)
                message = f"NEVER USED: {var_name} was written at IID {iid} with value {val} but never read until program end"
                self.log(message)
                # 添加到未使用变量列表
                self.unused_vars[var_name] = (iid, val)

        # 汇总报告
        if len(self.unused_vars) > 0:
            self.log(f"Found {len(self.unused_vars)} unused variables in total:")

            # 报告被覆盖的变量
            overwritten_vars = {k: v for k, v in self.unused_vars.items() if k not in never_used_vars}
            if overwritten_vars:
                self.log(f"  Variables overwritten before being used: {len(overwritten_vars)}")
                for var_name, (iid, val) in overwritten_vars.items():
                    self.log(f"  - {var_name} written at IID {iid} with value {val} but overwritten before being read")

            # 报告从未使用的变量
            if never_used_vars:
                self.log(f"  Variables never used until program end: {len(never_used_vars)}")
                for var_name, (iid, val) in never_used_vars.items():
                    self.log(f"  - {var_name} written at IID {iid} with value {val} but never read")
        else:
            self.log("No unused variables detected.")

        self.log(f"Total write operations tracked: {len(self.write_ops)}")
        self.log(f"Total read operations tracked: {len(self.read_ops)}")

        logging.shutdown()
