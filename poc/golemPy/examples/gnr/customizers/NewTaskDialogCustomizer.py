import os
from PyQt4 import QtCore
from PyQt4.QtGui import QFileDialog

from NewTaskDialog import NewTaskDialog
from AddTaskResourcesDialog import AddTaskResourcesDialog
from ShowTaskResourcesDialog import ShowTaskResourcesDialog

from AddResourcesDialogCustomizer import AddResourcesDialogCustomizer

from TaskTableElem import TaskTableElem


class NewTaskDialogCustomizer:
    #############################
    def __init__( self, gui, logic ):

        assert isinstance( gui, NewTaskDialog )

        self.gui    = gui
        self.logic  = logic

        self.__setupConnections()

        self.__init()

        self.resources                  = set()
        self.addTaskResourceDialog      = None
        self.taskState                  = None

    #############################
    def __setupConnections( self ):
        QtCore.QObject.connect( self.gui.ui.rendereComboBox, QtCore.SIGNAL( "currentIndexChanged( const QString )" ), self.__rendererComboBoxValueChanged )
        self.gui.ui.chooseOutputFileButton.clicked.connect( self.__chooseOutputFileButtonClicked ) 
        self.gui.ui.chooseMainProgramFileButton.clicked.connect( self.__choosMainProgramFileButtonClicked )
        self.gui.ui.addResourceButton.clicked.connect( self.__showAddResourcesDialog )
        self.gui.ui.showResourceButton.clicked.connect( self.__showShowResourcesDialog )
        self.gui.ui.testTaskButton.clicked.connect( self.__testTaskButtonClicked )
        self.gui.ui.finishBatton.clicked.connect( self.__finishButtonClicked )

    #############################
    def __updateRendererOptions( self, name ):
        r = self.logic.getRenderer( name )

        if r:
            self.logic.setCurrentRenderer( name )
            self.gui.ui.pixelFilterComboBox.clear()
            self.gui.ui.pixelFilterComboBox.addItems( r.filters )

            self.gui.ui.pathTracerComboBox.clear()
            self.gui.ui.pathTracerComboBox.addItems( r.pathTracers )

            self.gui.ui.outputFormatsComboBox.clear()
            self.gui.ui.outputFormatsComboBox.addItems( r.outputFormats )

            for i in range( len( r.outputFormats ) ):
                if r.outputFormats[ i ] == r.defaults.outputFormat:
                    self.gui.ui.outputFormatsComboBox.setCurrentIndex( i )

            self.gui.ui.mainProgramFileLineEdit.setText( r.defaults.mainProgramFile )

            time = QtCore.QTime()
            self.gui.ui.fullTaskTimeoutTimeEdit.setTime( time.addSecs( r.defaults.fullTaskTimeout ) )
            self.gui.ui.subtaskTimeoutTimeEdit.setTime( time.addSecs( r.defaults.subtaskTimeout ) )
            self.gui.ui.minSubtaskTimeTimeEdit.setTime( time.addSecs( r.defaults.minSubtaskTime ) )

        else:
            assert False, "Unreachable"


    # SLOTS
    #############################
    def __taskTableRowClicked( self, row ):
        if row < self.gui.ui.renderTaskTableWidget.rowCount():
            taskId = self.gui.ui.renderTaskTableWidget.item( row, 0 ).text()
            taskId = "{}".format( taskId )
            self.updateTaskAdditionalInfo( taskId )

    #############################
    def __showNewTaskDialogClicked( self ):
        renderers = self.logic.getRenderers()
            
        self.__setupNewTaskDialogConnections( self.gui.ui )

        self.gui.ui.taskIdLabel.setText( self.__generateNewTaskUID() )

        for k in renderers:
            r = renderers[ k ]
            self.gui.ui.rendereComboBox.addItem( r.name )

        testTasks = self.logic.getTestTasks()
        for k in testTasks:
            tt = testTasks[ k ]
            self.gui.ui.testTaskComboBox.addItem( tt.name )

    #############################
    def __rendererComboBoxValueChanged( self, name ):
        self.__updateRendererOptions( "{}".format( name ) )

    #############################
    def __chooseOutputFileButtonClicked( self ):

        cr = self.logic.getCurrentRenderer()

        outputFileType = "{}".format( self.gui.ui.outputFormatsComboBox.currentText() )
        filter = "{} (*.{})".format( outputFileType, outputFileType )

        dir = os.path.dirname( "{}".format( self.gui.ui.outputFileLineEdit.text() )  )

        fileName = "{}".format( QFileDialog.getSaveFileName( self.gui.window,
            "Choose output file", dir, filter ) )

        self.gui.ui.outputFileLineEdit.setText( fileName )

    #############################
    def __choosMainProgramFileButtonClicked( self ):

        dir = os.path.dirname( "{}".format( self.gui.ui.mainProgramFileLineEdit.text() )  )

        fileName = QFileDialog.getOpenFileName( self.gui.window,
            "Choose main program file", dir, "Python (*.py)")

        self.gui.ui.outputFileLineEdit.setText( fileName )

    ############################
    def __showAddResourcesDialog( self ):
        if not self.addTaskResourceDialog:
            self.addTaskResourceDialog = AddTaskResourcesDialog( self.gui.window )
            self.addTaskResourcesDialogCustomizer = AddResourcesDialogCustomizer( self.addTaskResourceDialog, self.logic )

        self.addTaskResourceDialog.show()

    ############################
    def __showShowResourcesDialog( self ):
        self.addTaskResourceDialog = ShowTaskResourcesDialog( self.gui.window )
        self.addTaskResourceDialog.show()

    ############################
    def __testTaskButtonClicked( self ):
        self.taskState = self.__queryTaskState()
        if self.logic.runTestTask( self.taskState ):
            self.gui.ui.finishBatton.setEnabled( True )
            self.gui.ui.testTaskButton.setEnabled( False )
        else:
            print "Task not tested properly"

    #############################
    def __finishButtonClicked( self ):
        self.logic.addTasks( [ self.taskState ] )
        self.gui.window.close()

    #############################
    def __generateNewTaskUID( self ):
        import uuid
        return "{}".format( uuid.uuid4() )

    #############################
    def __init( self ):
        renderers = self.logic.getRenderers()

        self.gui.ui.taskIdLabel.setText( self.__generateNewTaskUID() )

        for k in renderers:
            r = renderers[ k ]
            self.gui.ui.rendereComboBox.addItem( r.name )

        testTasks = self.logic.getTestTasks()
        for k in testTasks:
            tt = testTasks[ k ]
            self.gui.ui.testTaskComboBox.addItem( tt.name )

    #############################
    def __queryTaskState( self ):
        self.taskState = Task
        pass





