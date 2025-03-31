from dynapyt.analyses.BaseAnalysis import BaseAnalysis

class ObjectCreationInLoopAnalysis(BaseAnalysis):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # 开启DEBUG模式
        self.debug = True

        # Loop tracking
        self.loop_stack = []
        self.loop_depth = 0

        # Track object creations by location and type
        self.object_creations = {}

        # Track objects created multiple times in the same loop
        self.repeated_creations = {}

        # Track objects by their memory address to detect new allocations
        self.objects_in_loop = {}

        # Keep track of variable assignments within loops
        self.loop_assignments = {}

        # Line numbers where objects are created
        self.creation_locations = {}

        # Track memory allocations in loops
        self.loop_allocations = []

    def enter_for(self, dyn_ast, iid, *args, **kwargs):
        if self.debug:
            print(f"[DEBUG] Entering for loop with iid {iid}, current loop_stack: {self.loop_stack}")
        # 检查整个循环栈中是否已存在当前 iid
        if any(existing_iid == iid for _, existing_iid in self.loop_stack):
            self._record_iteration(iid)
            if self.debug:
                print(f"[DEBUG] Iteration recorded in for loop with iid {iid}")
        else:
            self.loop_depth += 1
            self.loop_stack.append(("for", iid))
            self._reset_loop_tracking(iid)
            if self.debug:
                print(f"[DEBUG] New for loop started. Loop depth: {self.loop_depth}")

    def enter_while(self, dyn_ast, iid, *args, **kwargs):
        if self.debug:
            print(f"[DEBUG] Entering while loop with iid {iid}, current loop_stack: {self.loop_stack}")
        # 检查整个循环栈中是否已存在当前 iid
        if any(existing_iid == iid for _, existing_iid in self.loop_stack):
            self._record_iteration(iid)
            if self.debug:
                print(f"[DEBUG] Iteration recorded in while loop with iid {iid}")
        else:
            self.loop_depth += 1
            self.loop_stack.append(("while", iid))
            self._reset_loop_tracking(iid)
            if self.debug:
                print(f"[DEBUG] New while loop started. Loop depth: {self.loop_depth}")

    def normal_exit_for(self, dyn_ast, iid, *args, **kwargs):
        if self.loop_stack and self.loop_stack[-1][1] == iid:
            if self.debug:
                print(f"[DEBUG] Exiting for loop with iid {iid}")
            loop_type, loop_iid = self.loop_stack.pop()
            self._analyze_loop_objects(loop_iid)
            self.loop_depth = max(0, self.loop_depth - 1)
            if self.debug:
                print(f"[DEBUG] For loop exited. Current loop depth: {self.loop_depth}")

    def normal_exit_while(self, dyn_ast, iid, *args, **kwargs):
        if self.loop_stack and self.loop_stack[-1][1] == iid:
            if self.debug:
                print(f"[DEBUG] Exiting while loop with iid {iid}")
            loop_type, loop_iid = self.loop_stack.pop()
            self._analyze_loop_objects(loop_iid)
            self.loop_depth = max(0, self.loop_depth - 1)
            if self.debug:
                print(f"[DEBUG] While loop exited. Current loop depth: {self.loop_depth}")

    def _break(self, dyn_ast, iid, *args, **kwargs):
        if self.loop_stack and self.loop_stack[-1][1] == iid:
            if self.debug:
                print(f"[DEBUG] Break encountered in loop with iid {iid}")
            loop_type, loop_iid = self.loop_stack.pop()
            self._analyze_loop_objects(loop_iid)
            self.loop_depth = max(0, self.loop_depth - 1)
            if self.debug:
                print(f"[DEBUG] Loop exited via break. Current loop depth: {self.loop_depth}")

    def _continue(self, dyn_ast, iid, *args, **kwargs):
        if self.loop_stack:
            loop_type, loop_iid = self.loop_stack[-1]
            self._record_iteration(loop_iid)
            if self.debug:
                print(f"[DEBUG] Continue in loop with iid {loop_iid}")

    def _list(self, dyn_ast, iid, val, *args, **kwargs):
        if self.loop_depth > 0 and val is not None:
            if self.debug:
                print(f"[DEBUG] List created in loop (iid {iid}).")
            self._record_object_creation("list", iid, val, dyn_ast)

    def _tuple(self, dyn_ast, iid, val, *args, **kwargs):
        if self.loop_depth > 0 and val is not None:
            if self.debug:
                print(f"[DEBUG] Tuple created in loop (iid {iid}).")
            self._record_object_creation("tuple", iid, val, dyn_ast)

    def _set(self, dyn_ast, iid, val, *args, **kwargs):
        if self.loop_depth > 0 and val is not None:
            if self.debug:
                print(f"[DEBUG] Set created in loop (iid {iid}).")
            self._record_object_creation("set", iid, val, dyn_ast)

    def dictionary(self, dyn_ast, iid, val, *args, **kwargs):
        if self.loop_depth > 0 and val is not None:
            if self.debug:
                print(f"[DEBUG] Dict created in loop (iid {iid}).")
            self._record_object_creation("dict", iid, val, dyn_ast)

    def write(self, dyn_ast, iid, old_vals, new_val, *args, **kwargs):
        if self.loop_depth > 0 and new_val is not None:
            obj_type = self._get_object_type(new_val)
            if obj_type and self.loop_stack:
                loop_iid = self.loop_stack[-1][1]
                if loop_iid not in self.loop_assignments:
                    self.loop_assignments[loop_iid] = {}
                key = f"{iid}:{obj_type}"
                if key not in self.loop_assignments[loop_iid]:
                    self.loop_assignments[loop_iid][key] = []
                self.loop_assignments[loop_iid][key].append(id(new_val))
                if self.debug:
                    print(f"[DEBUG] Variable assignment in loop (iid {loop_iid}): key {key} id {id(new_val)}")
                if len(self.loop_assignments[loop_iid][key]) > 1:
                    addresses = set(self.loop_assignments[loop_iid][key])
                    if len(addresses) > 1:
                        if key not in self.repeated_creations:
                            self.repeated_creations[key] = {
                                'count': 0,
                                'locations': [],
                                'type': obj_type,
                                'iid': iid,
                                'dyn_ast': dyn_ast
                            }
                        self.repeated_creations[key]['count'] += 1
                        try:
                            import ast
                            with open(dyn_ast, 'r') as f:
                                tree = ast.parse(f.read())
                            for node in ast.walk(tree):
                                if hasattr(node, 'lineno') and getattr(node, 'lineno', 0) > 0:
                                    self.repeated_creations[key]['locations'].append(node.lineno)
                                    break
                        except:
                            pass

    def memory_access(self, dyn_ast, iid, val, *args, **kwargs):
        if self.loop_depth > 0 and val is not None:
            obj_type = self._get_object_type(val)
            if obj_type and obj_type in ('list', 'dict', 'set', 'tuple'):
                self.loop_allocations.append({
                    'iid': iid,
                    'type': obj_type,
                    'size': self._estimate_object_size(val),
                    'obj_id': id(val)
                })
                if self.debug:
                    print(f"[DEBUG] Memory access recorded for {obj_type} (iid {iid}, size {self._estimate_object_size(val)})")

    def end_execution(self, *args, **kwargs):
        if self.repeated_creations:
            print("\n=== Object Creation in Loops Analysis ===\n")
            print("Detected repeated object creation in loops:")
            for key, data in self.repeated_creations.items():
                obj_type = data['type']
                count = data['count']
                locations = set(data['locations'])
                if count >= 3:
                    location_str = ', '.join(map(str, locations)) if locations else "unknown"
                    print(f"  - {obj_type} created repeatedly ({count} times) at line(s): {location_str}")
                    print("    Impact: Increased memory allocation and garbage collection overhead")
                    if obj_type == 'list':
                        print("    Suggestion: Move list creation outside the loop and clear it between iterations if needed")
                        print("               Consider using list comprehension instead of building list in loop")
                    elif obj_type == 'dict':
                        print("    Suggestion: Create the dictionary before the loop and update it inside")
                    elif obj_type == 'set':
                        print("    Suggestion: Initialize the set outside the loop, or use set comprehension")
                    print()
            print("\nGeneral advice for improving loop performance:")
            print("1. Move object creation outside loops when possible")
            print("2. Use comprehensions (list/dict/set) instead of building collections in loops")
            print("3. Consider using generators for large data processing")
            print("4. Preallocate containers to their expected size when possible")

    def _reset_loop_tracking(self, loop_iid):
        if loop_iid not in self.objects_in_loop:
            self.objects_in_loop[loop_iid] = {}
        if self.debug:
            print(f"[DEBUG] Loop tracking reset for iid {loop_iid}")

    def _record_object_creation(self, obj_type, iid, value, dyn_ast):
        if not self.loop_stack:
            return
        loop_iid = self.loop_stack[-1][1]
        key = f"{iid}:{obj_type}"
        if loop_iid not in self.object_creations:
            self.object_creations[loop_iid] = {}
        if key not in self.object_creations[loop_iid]:
            self.object_creations[loop_iid][key] = []
        self.object_creations[loop_iid][key].append(id(value))
        if self.debug:
            print(f"[DEBUG] Recorded creation of {obj_type} (key {key}, object id {id(value)}) in loop iid {loop_iid}")
        try:
            import ast
            with open(dyn_ast, 'r') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if hasattr(node, 'lineno') and getattr(node, 'lineno', 0) > 0:
                    if key not in self.creation_locations:
                        self.creation_locations[key] = set()
                    self.creation_locations[key].add(node.lineno)
                    break
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Failed to record creation location: {e}")

    def _record_iteration(self, loop_iid):
        if loop_iid in self.objects_in_loop:
            self.objects_in_loop[loop_iid]['iterations'] = self.objects_in_loop[loop_iid].get('iterations', 0) + 1
        if self.debug:
            print(f"[DEBUG] Loop iid {loop_iid} iteration count: {self.objects_in_loop[loop_iid].get('iterations')}")

    def _analyze_loop_objects(self, loop_iid):
        if self.debug:
            print(f"[DEBUG] Analyzing objects in loop iid {loop_iid}")
        if loop_iid in self.object_creations:
            for key, obj_ids in self.object_creations[loop_iid].items():
                if len(set(obj_ids)) > 1:
                    obj_type = key.split(':')[1]
                    if key not in self.repeated_creations:
                        self.repeated_creations[key] = {
                            'count': len(obj_ids),
                            'type': obj_type,
                            'locations': list(self.creation_locations.get(key, [])) if key in self.creation_locations else [],
                            'iid': int(key.split(':')[0])
                        }
                    if self.debug:
                        print(f"[DEBUG] Detected repeated creation for {key}: count {len(obj_ids)}")

    def _get_object_type(self, obj):
        if isinstance(obj, list):
            return "list"
        elif isinstance(obj, dict):
            return "dict"
        elif isinstance(obj, set):
            return "set"
        elif isinstance(obj, tuple):
            return "tuple"
        return None

    def _estimate_object_size(self, obj):
        try:
            import sys
            return sys.getsizeof(obj)
        except:
            if isinstance(obj, list):
                return 64 + sum(self._estimate_object_size(x) for x in obj[:10]) * (len(obj) / 10 if len(obj) > 10 else 1)
            elif isinstance(obj, dict):
                return 240 + len(obj) * 24
            elif isinstance(obj, set):
                return 224 + len(obj) * 8
            elif isinstance(obj, tuple):
                return 64 + sum(self._estimate_object_size(x) for x in obj[:10]) * (len(obj) / 10 if len(obj) > 10 else 1)
            return 24
