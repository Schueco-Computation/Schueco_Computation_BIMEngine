
# Enable Python support and load DesignScript library
import clr

# Import docManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#End Transaction
t1 = TransactionManager.Instance
TransactionManager.ForceCloseTransaction(t1)

