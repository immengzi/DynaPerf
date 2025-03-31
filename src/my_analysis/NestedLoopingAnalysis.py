from dynapyt.analyses.BaseAnalysis import BaseAnalysis
from typing import Any, Optional, Iterable
import sys

class NestedLoopingAnalysis(BaseAnalysis):
    def __init__(self, depth_threshold: int = 2, **kwargs) -> None:
        super().__init__(**kwargs)

        # Dictionary to record loop count and occurrence
        self.active_loops = {}  # {(file_path, iid): {"type": "for/while", "count": 1, "depth": 1}}

        # Record the loop hierarchy - each loop ID maps to its parent loop ID
        self.loop_hierarchy = {}  # {(file_path, iid): (parent_file_path, parent_iid)}

        # Store nested structure
        self.loop_data = {}  # Stores information about each loop
        self.max_depth_seen = 0  # Tracks the maximum nested depth
        self.depth_threshold = depth_threshold  # Threshold setting
        self.nested_loops_detected = set()  # Records detected nested loops
        self.break_continue_stats = {}  # Tracks break and continue usage in loops

        # Debugging and safety measures
        self.currently_processing = False

    def enter_for(self, dyn_ast: str, iid: int, next_value: Any, iterable: Iterable) -> Optional[Any]:
        """Record entering for loop"""
        if self.currently_processing:
            return None

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)

            # Initialize loop if it is seen for the first time
            if loop_id not in self.active_loops:
                # Find the parent loop (the deepest active loop)
                parent_loop = None
                max_depth = -1

                for other_id, other_loop in self.active_loops.items():
                    if other_id != loop_id and other_loop["depth"] > max_depth:
                        parent_loop = other_id
                        max_depth = other_loop["depth"]

                depth = 1
                if parent_loop:
                    self.loop_hierarchy[loop_id] = parent_loop
                    depth = self.active_loops[parent_loop]["depth"] + 1

                self.active_loops[loop_id] = {
                    "type": "for",
                    "count": 1,
                    "depth": depth,
                    "iterations": []
                }

                # If depth exceeds the threshold, record as nested loop
                if depth >= self.depth_threshold:
                    self.currently_processing = False
                    self._record_nested_structure(loop_id)
            else:
                # Loop is already active, increment the count
                self.active_loops[loop_id]["count"] += 1

            # Record iteration value
            try:
                self.active_loops[loop_id]["iterations"].append(str(next_value))
            except:
                self.active_loops[loop_id]["iterations"].append("<non-serializable>")

            # Update max depth
            current_depth = self.active_loops[loop_id]["depth"]
            if current_depth > self.max_depth_seen:
                self.max_depth_seen = current_depth
        except Exception as e:
            print(f"Error: enter_for execution exception: {e}")
        finally:
            self.currently_processing = False

        return None

    def exit_for(self, dyn_ast: str, iid: int) -> None:
        """Record exiting for loop"""
        if self.currently_processing:
            return

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)
            if loop_id in self.active_loops:
                depth = self.active_loops[loop_id]["depth"]

                # Remove from active loops
                self.active_loops.pop(loop_id)

                # Also clear its children loops (if any)
                children_to_remove = []
                for child_id, parent_id in self.loop_hierarchy.items():
                    if parent_id == loop_id:
                        children_to_remove.append(child_id)

                for child_id in children_to_remove:
                    if child_id in self.active_loops:
                        self.active_loops.pop(child_id)
        except Exception as e:
            print(f"Error: exit_for execution exception: {e}")
        finally:
            self.currently_processing = False

    def normal_exit_for(self, dyn_ast: str, iid: int) -> None:
        """Record normal exit from for loop"""
        if self.currently_processing:
            return

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)
            if loop_id not in self.break_continue_stats:
                self.break_continue_stats[loop_id] = {"normal_exits": 0, "breaks": 0, "continues": 0}
            self.break_continue_stats[loop_id]["normal_exits"] += 1
        except Exception as e:
            print(f"Error: normal_exit_for execution exception: {e}")
        finally:
            self.currently_processing = False

    def enter_while(self, dyn_ast: str, iid: int, cond_value: bool) -> Optional[bool]:
        """Record entering while loop"""
        if self.currently_processing:
            return None

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)

            # Initialize loop if it is seen for the first time
            if loop_id not in self.active_loops:
                # Find the parent loop (the deepest active loop)
                parent_loop = None
                max_depth = -1

                for other_id, other_loop in self.active_loops.items():
                    if other_id != loop_id and other_loop["depth"] > max_depth:
                        parent_loop = other_id
                        max_depth = other_loop["depth"]

                depth = 1
                if parent_loop:
                    self.loop_hierarchy[loop_id] = parent_loop
                    depth = self.active_loops[parent_loop]["depth"] + 1

                self.active_loops[loop_id] = {
                    "type": "while",
                    "count": 1,
                    "depth": depth,
                    "conditions": [cond_value]
                }

                # If depth exceeds the threshold, record as nested loop
                if depth >= self.depth_threshold:
                    self._record_nested_structure(loop_id)
            else:
                # Loop is already active, increment the count
                self.active_loops[loop_id]["count"] += 1
                self.active_loops[loop_id]["conditions"].append(cond_value)

            # Update max depth
            current_depth = self.active_loops[loop_id]["depth"]
            if current_depth > self.max_depth_seen:
                self.max_depth_seen = current_depth
        except Exception as e:
            print(f"Error: enter_while execution exception: {e}")
        finally:
            self.currently_processing = False

        return None

    def exit_while(self, dyn_ast: str, iid: int) -> None:
        """Record exiting while loop"""
        if self.currently_processing:
            return

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)
            if loop_id in self.active_loops:
                depth = self.active_loops[loop_id]["depth"]

                # Remove from active loops
                self.active_loops.pop(loop_id)

                # Also clear its children loops (if any)
                children_to_remove = []
                for child_id, parent_id in self.loop_hierarchy.items():
                    if parent_id == loop_id:
                        children_to_remove.append(child_id)

                for child_id in children_to_remove:
                    if child_id in self.active_loops:
                        self.active_loops.pop(child_id)
        except Exception as e:
            print(f"Error: exit_while execution exception: {e}")
        finally:
            self.currently_processing = False

    def normal_exit_while(self, dyn_ast: str, iid: int) -> None:
        """Record normal exit from while loop"""
        if self.currently_processing:
            return

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, iid)
            if loop_id not in self.break_continue_stats:
                self.break_continue_stats[loop_id] = {"normal_exits": 0, "breaks": 0, "continues": 0}
            self.break_continue_stats[loop_id]["normal_exits"] += 1
        except Exception as e:
            print(f"Error: normal_exit_while execution exception: {e}")
        finally:
            self.currently_processing = False

    def _break(self, dyn_ast: str, iid: int, loop_iid: int) -> Optional[bool]:
        """Record break statement"""
        if self.currently_processing:
            return None

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, loop_iid)

            if loop_id not in self.break_continue_stats:
                self.break_continue_stats[loop_id] = {"normal_exits": 0, "breaks": 0, "continues": 0}
            self.break_continue_stats[loop_id]["breaks"] += 1
        except Exception as e:
            print(f"Error: _break execution exception: {e}")
        finally:
            self.currently_processing = False

        return None

    def _continue(self, dyn_ast: str, iid: int, loop_iid: int) -> Optional[bool]:
        """Record continue statement"""
        if self.currently_processing:
            return None

        self.currently_processing = True

        try:
            loop_id = (dyn_ast, loop_iid)

            if loop_id not in self.break_continue_stats:
                self.break_continue_stats[loop_id] = {"normal_exits": 0, "breaks": 0, "continues": 0}
            self.break_continue_stats[loop_id]["continues"] += 1
        except Exception as e:
            print(f"Error: _continue execution exception: {e}")
        finally:
            self.currently_processing = False

        return None

    def _get_loop_chain(self, loop_id):
        """Get the complete chain from the outermost to the current loop"""
        chain = []
        current = loop_id

        # Prevent infinite loop
        visited = set()

        while current and current not in visited:
            chain.append(current)
            visited.add(current)
            current = self.loop_hierarchy.get(current)

        # Reverse the chain to display from outer to inner
        chain.reverse()
        return chain

    def _record_nested_structure(self, loop_id):
        if self.currently_processing:
            return None

        self.currently_processing = True

        try:
            loop_chain = self._get_loop_chain(loop_id)

            # Ensure all loops in the chain are active
            for l_id in loop_chain:
                if l_id not in self.active_loops:
                    return

            # Ensure chain length exceeds threshold
            if len(loop_chain) >= self.depth_threshold:
                signature = tuple(loop_chain)

                if signature not in self.nested_loops_detected:
                    self.nested_loops_detected.add(signature)

                    # Record outer loop information
                    outer_loop_id = loop_chain[0]
                    outer_loop = self.active_loops.get(outer_loop_id)
                    if not outer_loop:
                        return

                    if outer_loop_id not in self.loop_data:
                        self.loop_data[outer_loop_id] = {
                            "type": outer_loop["type"],
                            "max_depth": len(loop_chain),
                            "nested_loops": []
                        }
                    else:
                        if len(loop_chain) > self.loop_data[outer_loop_id]["max_depth"]:
                            self.loop_data[outer_loop_id]["max_depth"] = len(loop_chain)

                    # Record inner loops
                    inner_loops = []
                    for i in range(1, len(loop_chain)):
                        inner_id = loop_chain[i]
                        inner_loop = self.active_loops.get(inner_id)
                        if not inner_loop:
                            continue
                        inner_loops.append((
                            inner_id[0],  # File path
                            inner_id[1],  # iid
                            inner_loop["type"]  # Loop type
                        ))

                    # Add to nested loop list to avoid duplicates
                    if inner_loops and inner_loops not in self.loop_data[outer_loop_id]["nested_loops"]:
                        self.loop_data[outer_loop_id]["nested_loops"].append(inner_loops)
        except Exception as e:
            print(f"Error: _record_nested_structure execution exception: {e}")
        finally:
            self.currently_processing = False

    def end_execution(self):
        """Generate report at the end of execution"""
        try:
            print("\n===== Nested Looping Analysis Report =====")

            if self.max_depth_seen >= self.depth_threshold:
                print(f"Warning: Possible performance issue - maximum nesting depth is {self.max_depth_seen}")

                # Ensure correct counting - use loop_data rather than nested_loops_detected
                total_nested_structures = sum(len(data["nested_loops"]) for data in self.loop_data.values())
                print(f"Detected {total_nested_structures} unique nested loop structures")

                # Detailed report for each outer loop and its nesting
                for loop_id, data in self.loop_data.items():
                    print(f"\nFor {loop_id[0]}: {data['type']} loop (iid: {loop_id[1]}):")
                    print(f"  Maximum nesting depth: {data['max_depth']}")
                    print(f"  Nested loop structures:")

                    for i, nested_loop in enumerate(data["nested_loops"]):
                        print(f"  Structure #{i+1}:")
                        for j, loop in enumerate(nested_loop):
                            print(f"    Level {j+1}: {loop[2]} loop at {loop[0]} (iid: {loop[1]})")

                    # Add break/continue stats
                    if loop_id in self.break_continue_stats:
                        stats = self.break_continue_stats[loop_id]
                        print(f"  Loop control flow stats:")
                        print(f"    Normal exits: {stats['normal_exits']}")
                        print(f"    Breaks: {stats['breaks']}")
                        print(f"    Continues: {stats['continues']}")

                        # Provide additional recommendations based on break/continue frequency
                        if stats.get('breaks', 0) > 5:
                            print("    Suggestion: High use of break may indicate optimization opportunities in the loop logic")
                        if stats.get('continues', 0) > 5:
                            print("    Suggestion: High use of continue may indicate filter conditions should be moved upfront")

                    # Performance recommendations
                    if data["max_depth"] >= 3:
                        print("  Performance suggestion: Consider refactoring code to reduce nesting depth, or use vectorization")
                    elif data["max_depth"] == 2:
                        print("  Performance suggestion: Monitor the performance of this double loop for large datasets")
            else:
                print(f"No loops exceeded the threshold depth ({self.depth_threshold}). Maximum nesting depth was {self.max_depth_seen}.")

            print("\n===== Analysis Complete =====")
        except Exception as e:
            print(f"Error: end_execution execution exception: {e}")
