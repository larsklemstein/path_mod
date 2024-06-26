if which path_mod.py >/dev/null
then
    # the --path option is a workarround for situations where 
    # a a pyhton wrapper (e.g. a pyenv shim) does modify the path
    # on it's own inside the python environment
    #
    PATH=$(path_mod.py --path="$PATH" unify)
fi

export PATH

