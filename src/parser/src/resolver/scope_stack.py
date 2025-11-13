class ScopeStack:
    """
    Manages a stack of scopes to enable lexical scoping for the resolver.
    
    This class encapsulates the environment logic, abstracting the
    implementation (a list of dictionaries) from the Resolver. Each scope
    in the stack is a dictionary mapping variable names (str) to their
    current resolution status (str, e.g., 'declared' or 'defined').
    """
    def __init__(self):
        """Initializes the ScopeStack and creates the global scope."""
        # The stack of scopes. Each item is a dictionary.
        self.scopes = []
        # Create the global scope
        self.push()
        self.define_natives()

    def define_natives(self):
        """
        Populates the global (outermost) scope with native functions
        that are implemented in the C++ interpreter.
        
        This prevents the resolver from raising 'undefined variable'
        errors for built-in functions like 'log' or 'input'.
        """
        self.declare("log")
        self.define("log")
        self.declare("logln")
        self.define("logln")
        self.declare("input")
        self.define("input")

    def push(self):
        """Pushes a new, empty scope onto the stack."""
        self.scopes.append({})

    def pop(self):
        """Pops the current scope off the stack."""
        if self.scopes:
            self.scopes.pop()

    def declare(self, name: str):
        """
        Declares a variable in the *current* (innermost) scope.
        
        This method is responsible for detecting re-declaration errors
        within the same local scope. Variables are marked as 'declared'
        but not yet 'defined'.
        
        Args:
            name: The string name of the variable to declare.
        
        Raises:
            Exception: If the variable is already declared in this scope.
        """
        if not self.scopes:
            return  # Global scope; no declaration needed.

        scope = self.scopes[-1]
        if name in scope:
            raise Exception(f"ResolverError: Variable '{name}' already defined in this scope.")
        scope[name] = "declared"

    def define(self, name: str):
        """
        Marks a variable as fully 'defined' in the current scope.
        
        This signifies that the variable's initializer (if any) has been
        processed and it is now available for use in subsequent statements.
        
        Args:
            name: The string name of the variable to define.
        """
        if not self.scopes:
            return # Global scope
            
        self.scopes[-1][name] = "defined"

    def is_defined(self, name: str) -> bool:
        """
        Checks if a variable is defined by traversing the scope stack backwards.
        
        This method implements the core logic of lexical scoping. It searches
        from the innermost scope to the outermost (global) scope. It also
        specifically raises an error if a variable is being accessed
        during its own declaration (i.e., its status is 'declared' but
        not yet 'defined').
        
        Args:
            name: The string name of the variable to look up.
            
        Returns:
            True if the variable is found and defined.
            
        Raises:
            Exception: If the variable is read in its own initializer.
            Exception: If the variable is not defined in any accessible scope.
        """
        if not self.scopes:
            return False
            
        # Check if the variable is being read in its own initializer
        if name in self.scopes[-1] and self.scopes[-1][name] == 'declared':
             raise Exception(f"ResolverError: Cannot read local variable '{name}' in its own initializer.")

        # Loop from the innermost scope outwards
        for scope in reversed(self.scopes):
            if name in scope:
                return True  # Found it!

        # If we finished the loop and found nothing, it's an error.
        raise Exception(f"ResolverError: Variable '{name}' is not defined.")