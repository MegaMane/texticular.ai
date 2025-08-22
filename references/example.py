class Example:
    """An Example Class representing a generic documentation template

    Provides some basic functionality for commands that can be used.
    As well as a class level dictionary that keeps track of all objects that are instantiated.

    Attributes
    -----------
    attribute1: list
        a list of dictionaries in the form of {col: val} for each successfully parsed item

    Methods
    ---------
    __init__()
        The constructor for the Example Class

    """

    def example_func(self, arg1: str, arg2: int = 2, *args, **kwargs) -> str:
        """An example function for the purpose of showing a docstring using numpy style

        Here is the extended explanation of the function where we can get into more detail
        if needed.

        Parameters
        -----------
        arg1: str
            The first argument it's a string
        arg2: int, optional
            The second argument. It's an int (default is 2)
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.

        Returns
        -----------
        str
            An example string printing the arguments passed in to the function

        Raises
        ----------
        ValueError
            If arg2 is < 0

        See Also
        ----------
        https://numpydoc.readthedocs.io/en/latest/format.html#references

        Examples
        ----------
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]


        Section breaks are created with two blank lines. Section breaks are also
        implicitly created anytime a new section starts. Section bodies *may* be
        indented:

        Notes
        -----------
            This is an example of an indented section. It's like any other section,
            but the body is indented to help it stand out from surrounding text.

        If a section is indented, then a section break is created by
        resuming unindented text
        """

        if arg2 < 0:
            raise ValueError("Negative values are not supported.")

        return f"You called example_func: arg1={arg1}, arg2={arg2}"