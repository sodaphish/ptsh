import imp, pkgutil, os, sys, types


def get_functions( module ):
    functionList = []
    for key, value in module.__dict__.items():
        if type( value ) is types.FunctionType:
            functionList.append( value )
    return functionList


def init_plugins( path='%s%splugins' % ( os.getcwd(), os.sep ) ):
	sys.path.append( path ) 
	for loader, packageName, ispkg in pkgutil.iter_modules( [ path ] ):
		f, filename, description = imp.find_module( packageName )
		loaded = imp.load_module( packageName, f, filename, description )
		for f in get_functions( loaded ):
			if f.__name__ is 'plugin_init':
				f()


if __name__ is '__main__':
	init_plugins()
