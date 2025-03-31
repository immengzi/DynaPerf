from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Any, List, Dict

class RecursionAnalysis(BaseAnalysis):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.call_stacks: Dict[str, Dict[int, int]] = {}
        self.threshold = 10
        self.reported = set()  # To avoid duplicate reporting

    def function_enter(self, dyn_ast: str, iid: int, args: List[Any], name: str, is_lambda: bool) -> None:
        # Initialize tracking for new functions
        if name not in self.call_stacks:
            self.call_stacks[name] = {}

        # Initialize depth counter for this call site
        if iid not in self.call_stacks[name]:
            self.call_stacks[name][iid] = 0

        self.call_stacks[name][iid] += 1

        # Check threshold and report once
        if self.call_stacks[name][iid] > self.threshold and (name, iid) not in self.reported:
            print(f"Recursion depth exceeded for function {name} at {iid}. Current depth: {self.call_stacks[name][iid]}")
            self.reported.add((name, iid))

    def function_exit(self, dyn_ast: str, function_iid: int, name: str, result: Any) -> Any:
        # Only modify tracked functions/call sites
        if name in self.call_stacks and function_iid in self.call_stacks[name]:
            self.call_stacks[name][function_iid] -= 1

            # Cleanup empty call sites
            if self.call_stacks[name][function_iid] == 0:
                del self.call_stacks[name][function_iid]

            # Cleanup empty functions
            if not self.call_stacks[name]:
                del self.call_stacks[name]

        return result
