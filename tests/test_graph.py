from app.graph.nodes import route_after_validation,route_after_tool_selection
def test_validation_routes(): assert route_after_validation({'errors':[]})=='planner'; assert route_after_validation({'errors':['x']})=='guardrail'
def test_approval_route(): assert route_after_tool_selection({'approval_required':True,'approved':False})=='approval'; assert route_after_tool_selection({'approval_required':True,'approved':True})=='research'
