from app.state import WorkflowState


def validate_dsl_node(state: WorkflowState):
       new_state = dict(state)

       workflow = state.get("dsl", {})
       errors=[]
       triggers = workflow.get("triggers", [])
       actions = workflow.get("actions", [])
       timeouts = workflow.get("timeouts", [])
       if len(triggers) == 0:
        errors.append("Workflow must contain at least 1 trigger.")

       if len(actions) == 0:
        errors.append("Workflow must contain at least 1 action.")

       action_names = [a["name"] for a in actions]

       valid_action_names = set(action_names)

       for tm in timeouts:
        if tm.get("after_minutes", -1) <= 0:
            errors.append(f"Timeout '{tm.get('name')}' must have a positive 'after_minutes'.")

        act = tm.get("action")
        if act and act not in valid_action_names:
            errors.append(
                f"Timeout '{tm.get('name')}' refers to unknown action '{act}'."
            )

        new_state["errors"] = errors
        new_state["valid"] = (len(errors) == 0)
       return new_state