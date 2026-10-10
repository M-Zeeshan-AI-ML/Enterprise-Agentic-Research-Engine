from alembic import op
import sqlalchemy as sa
revision='0001_initial'; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
 op.create_table('research_executions',sa.Column('id',sa.String(36),primary_key=True),sa.Column('conversation_id',sa.String(255),nullable=False),sa.Column('user_id',sa.String(255),nullable=False),sa.Column('question',sa.Text(),nullable=False),sa.Column('status',sa.String(40),nullable=False),sa.Column('result',sa.JSON(),nullable=True),sa.Column('error',sa.Text(),nullable=True),sa.Column('request_id',sa.String(64),nullable=True),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False),sa.Column('tool_calls',sa.Integer(),nullable=False))
 op.create_index('ix_research_executions_conversation_id','research_executions',['conversation_id']); op.create_index('ix_research_executions_user_id','research_executions',['user_id']); op.create_index('ix_research_executions_status','research_executions',['status'])
def downgrade(): op.drop_table('research_executions')
