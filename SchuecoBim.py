import sys
sys.path.append("Modules\\Rhino_modules")
sys.path.append("Modules\\Rhino_Revit_Modules")
sys.path.append("Objects")
import blockorg
import corners
import simplify
# import ConvertPoly
# import CreateExtrusion
# import CreateFamily
import Profile
# def __reverse_modulesearch(func_name):
#     if func_name is None: return None
#     if not isinstance(func_name, basestring): return None
#     g_lower = dict((k.lower(),(k,v)) for k,v in globals().items())
#     f_lower = func_name.lower()
#     if f_lower in g_lower:
#         f_data = g_lower[f_lower]
#         if f_data[1]:
#             try:
#                 full_module_name = f_data[1].__module__
#                 if full_module_name: return (f_data[0],full_module_name)
#             except:
#                 return None
# if __name__== "main":
#     from Profile import Profile