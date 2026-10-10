from app.graph.nodes import route_after_approval
def test_rejected_approval_stops(): assert route_after_approval({'approved':False})=='guardrail'
def test_approved_continues(): assert route_after_approval({'approved':True})=='research'
