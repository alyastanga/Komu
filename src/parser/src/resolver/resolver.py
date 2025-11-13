# Komu/src/parser/src/resolver.py
from ..nodes.statement_nodes import (
    MissionNode, VarAssignNode, AssignNode, ReturnNode, WhileNode, ConditionalNode, MissionCallNode
)
from ..nodes.literal_nodes import IdentifierNode
from ..nodes.expression_nodes import * 
from .scope_stack import ScopeStack  

class Resolver:
    """
    Performs static analysis on the AST to resolve all variables.
    
    This class traverses the Abstract Syntax Tree (AST) using the
    Visitor pattern. Its primary responsibility is to ensure that all
    variable declarations, assignments, and usages are valid according to
    the language's scoping rules. It relies on a `ScopeStack` instance
    to manage the environment state.
    """
    def __init__(self):
        """Initializes the Resolver and its associated ScopeStack."""
        self.scope_stack = ScopeStack()

    def resolve(self, statements: list):
        """
        The main entry point for the resolver.
        
        Args:
            statements: A list of top-level AST statement nodes.
        """
        for statement in statements:
            self.visit(statement)

    def visit(self, node):
        """
        Generic visitor dispatch method.
        
        It dynamically constructs the name of the appropriate visitor method
        based on the node's class name (e.g., `VarAssignNode` becomes
        `visit_VarAssignNode`) and calls it. If no specific visitor method
        is found, it falls back to `generic_visit`.
        
        Args:
            node: The AST node to visit.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        method(node)

    def generic_visit(self, node):
        """
        Fallback visitor method for AST nodes that do not require
        specific resolution logic.
        """
        pass # Silently ignore nodes we don't care about

    # --- Scope-Modifying Statements ---

    def visit_MissionNode(self, node: MissionNode):
        """
        Resolves a mission (function) definition.
        
        This process involves:
        1. Declaring and defining the mission's name in the current scope
           (to allow for recursive calls).
        2. Pushing a new scope for the mission's body.
        3. Declaring and defining all parameters within that new scope.
        4. Resolving the list of statements in the mission's body.
        5. Popping the mission's scope upon completion.
        """
        # 1. Declare and define the mission's name in the current scope
        self.scope_stack.declare(node.identifier.name)
        self.scope_stack.define(node.identifier.name)

        # 2. Create a NEW scope for the mission's body
        self.scope_stack.push()

        # 3. Add parameters to the new scope
        if node.parameter:
            for param in node.parameter:
                self.scope_stack.declare(param.name)
                self.scope_stack.define(param.name)
        
        # 4. Resolve the mission's body in that new scope
        self.resolve(node.body)

        # 5. Exit the mission's scope
        self.scope_stack.pop()

    def visit_WhileNode(self, node: WhileNode):
        """Resolves a while loop statement."""
        self.visit(node.condition)
        self.resolve(node.body) # body is a list of statements

    def visit_ConditionalNode(self, node: ConditionalNode):
        """Resolves an if-else conditional statement."""
        self.visit(node.if_condition)
        self.resolve(node.if_body)
        if node.else_body:
            self.resolve(node.else_body)
        # Note: A full implementation would also iterate over else_if blocks.

    def visit_ReturnNode(self, node: ReturnNode):
        """Resolves a return statement."""
        if node.value:
            self.visit(node.value)

    # --- Variable and Assignment Statements ---

    def visit_VarAssignNode(self, node: VarAssignNode):
        """
        Resolves a variable declaration (e.g., 'var h = 2;').
        
        It first resolves the initializer expression, then declares
        and defines the new variable in the current scope. This ordering
        ensures that a variable is not available in its own initializer.
        """
        # 1. Resolve the value it's being assigned to
        self.visit(node.value)

        # 2. Add the new variable to the current scope
        self.scope_stack.declare(node.identifier.name)
        self.scope_stack.define(node.identifier.name)

    def visit_AssignNode(self, node: AssignNode):
        """
        Resolves a variable assignment (e.g., 'h = 5;').
        
        It resolves the right-hand-side expression and then verifies
        that the target variable (e.g., 'h') is already defined in an
        accessible scope.
        """
        # 1. Resolve the new value
        self.visit(node.value)
        # 2. Check that the variable being assigned to exists
        self.scope_stack.is_defined(node.identifier.name)


    def visit_IdentifierNode(self, node: IdentifierNode):
        """
        Resolves a variable *read* (e.g., as used in 'logln(h)').
        
        This is the primary read operation. It checks the scope stack
        to ensure the variable is defined and accessible from this point.
        """
        self.scope_stack.is_defined(node.name)

    def visit_MissionCallNode(self, node: MissionCallNode):
        """Resolves a mission (function) call."""
        # Resolve the function name itself (e.g., 'log', 'test')
        self.visit(node.identifier) 
        
        # Resolve all argument expressions
        if node.argument:
            for arg in node.argument:
                self.visit(arg)

    # --- Expression Nodes ---
    
    def visit_BinaryOpNode(self, node: BinaryOpNode):
        """Resolves both sides of a binary operation."""
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_RelationalOpNode(self, node: RelationalOpNode):
        """Resolves both sides of a relational operation."""
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_LogicalOpNode(self, node: LogicalOpNode):
        """Resolves both sides of a logical operation."""
        self.visit(node.left_node)
        self.visit(node.right_node)
        
    def visit_BitwiseOpNode(self, node: BitwiseOpNode):
        """Resolves both sides of a bitwise operation."""
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        """Resolves the operand of a unary operation."""
        self.visit(node.node)
        
    def visit_PostfixUnaryOpNode(self, node: PostfixUnaryOpNode):
        """Resolves the operand of a postfix unary operation."""
        self.visit(node.node)