import sys, os
sys.path.append( os.getcwd() )
from Registry import *
from Plugins import *
from Logger import *
from javax.swing import *
from java.awt import *
from javax.swing.tree import DefaultMutableTreeNode

reg = Registry()
conf = []
conf = reg.getScope( "global.%" )
logger = Logger( ["f", conf['global.logfile'] ] )
logger.setLevel( conf['global.loglevel'] )

logger.debug( "__BEGIN__" )

# put your code here.



class jTODO: 

	def addContext( self, branch, branchData=None ):
		if branchData == None:
			branch.add( DefaultMutableTreeNode( 'No valid Data' ) )
		else:
			for item in branchData:
				branch.add( DefaultMutableTreeNode( item ) )

	def __init__( self ):
		frame = JFrame( "jTODO", defaultCloseOperation=JFrame.EXIT_ON_CLOSE, size=(400,350), layout=BorderLayout() )


		treeTrunk = DefaultMutableTreeNode( 'Contexts' )
		treeTrunk.add( DefaultMutableTreeNode( 'Sample Context' ) )
		self.tree = JTree( treeTrunk )

		leftPanel = JPanel()
		leftScrollPane = JScrollPane( self.tree )
		#leftScrollPane.setPreferredSize( Dimension( 300,250 ) )
		leftScrollPane.getViewport().setView( (self.tree) )

		leftPanel.add( leftScrollPane ) 


		label2 = JLabel( "right" )
		rightPanel = JPanel()
		rightPanel.add( label2 )


		splitPane = JSplitPane( JSplitPane.HORIZONTAL_SPLIT )
		splitPane.setLeftComponent( leftPanel )
		splitPane.setRightComponent( rightPanel )
		#splitPane.setDividerLocation( 200 )

		frame.add( splitPane )
		frame.setDefaultCloseOperation( WindowConstants.EXIT_ON_CLOSE )
		frame.show()

		
if __name__ == '__main__':
	jTODO()


# end your code here

logger.debug( "__END__" )
'''__EOF__'''
