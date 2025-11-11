"""
Compatibility shim for MarkupSafe using built-in html module
This allows Flask to work without installing the MarkupSafe package
which requires C++ compiler on Windows
"""

import html
import sys

class Markup(str):
    """
    Simple Markup string class compatible with MarkupSafe.Markup
    Subclasses str and marks it as "safe" HTML
    """
    __slots__ = ()
    
    def __html__(self):
        return str(self)
    
    @staticmethod
    def escape(s=None):
        """Escape HTML characters"""
        if s is None:
            return Markup("")
        if isinstance(s, Markup):
            return s
        return Markup(html.escape(str(s) if s is not None else ''))

# Functions and classes needed by Jinja2
def soft_str(s):
    """Convert to string (soft_str in MarkupSafe)"""
    if isinstance(s, Markup):
        return s
    return str(s) if s is not None else ''

def soft_unicode(s):
    """Alias for soft_str (old name)"""
    return soft_str(s)

def escape(s):
    """Module level escape function"""
    return Markup.escape(s)

# Create module mock
class MarkupSafeModule:
    Markup = Markup
    escape = staticmethod(escape)
    soft_str = soft_str
    soft_unicode = soft_unicode
    
    def __getattr__(self, name):
        raise AttributeError(f"module 'markupsafe' has no attribute '{name}'")

# Inject into sys.modules before Flask imports it
sys.modules['markupsafe'] = MarkupSafeModule()
