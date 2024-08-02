import sys, os, argparse, prettytable, time
from pymongo import MongoClient
import pathlib, datetime, threading, pymongo, bson



# arguments
tmpl = ""
with open("templates/arguments.py", "r") as file:
  tmpl = "".join(file.readlines())
exec(tmpl)

snme = "serv"                                   
lnme = "server"                       
desc = "source watcher"              
auth.append("Huseyin YIGIT, yigit.hsyn@gmail.com")

# prepare arguments
tmpl = ""
with open("templates/prepare_arguments.py", "r") as file:
  tmpl = "".join(file.readlines())
exec(tmpl)

# argument parsing 
tmpl = ""
with open("templates/argument_parsing.py", "r") as file:
  tmpl = "".join(file.readlines())
exec(tmpl)

# implementation
mgcl = MongoClient()
mgdb = mgcl["sources"]

def chck():
  global thrr
  while thrr:
    for item in mgdb.get_collection("project").find({}):
      path = pathlib.Path("D:/00 PROJELER/").joinpath(item["project"]).joinpath("/".join(item["categories"]),item["name"])
      if not path.exists(follow_symlinks=False):
        print("Path does not exists any more")
        mgdb.get_collection("project").delete_one({"_id": bson.ObjectId(item["_id"])})
      else:
        pass
      if not thrr:
        break


def updt():
  global  thrr
  while thrr:
    ptrn = "PDF Document"
    for item in pathlib.Path("D:/00 PROJELER/").rglob("*.pdf"):
      stat = item.stat()
      obje = {
        "pattern"   : ptrn,
        "name"      : item.name,
        "project"   : item.parts[2],
        "categories": item.parts[3:-1],
        "size"      : stat.st_size,
        "c_time"    : 0,
        "m_time"    : stat.st_mtime,
        "a_time"    : stat.st_atime,
      }
      try:
        obje["c_time"] = stat.st_birthtime
      except:
        obje["c_time"] = stat.st_ctime
      
      fobj = mgdb.get_collection("project").find_one({ "pattern"   : obje["pattern"],
                                                       "name"      : obje["name"],
                                                       "project"   : obje["project"],
                                                       "categories": obje["categories"]
                                                    })
      if fobj:
        if fobj["c_time"] != obje["c_time"] or fobj["m_time"] != obje["m_time"] or fobj["a_time"] != obje["a_time"]:
          print("Change in sources")
          mgdb.get_collection("project").update_one({"_id": bson.ObjectId(fobj["_id"])}, {"$set": {"c_time": obje["c_time"], "m_time": obje["m_time"], "a_time": obje["a_time"] }})
      else:
        mgdb.get_collection("project").insert_one(obje)
      if not thrr:
        break


thrr = True

thr1 = threading.Thread(target=chck, name='Continous check')
thr1.start()

thr2 = threading.Thread(target=updt, name='Continous update')
thr2.start()

print("Type 'exit' to terminate.")
while thrr:
  cmnd = input()
  if cmnd == "exit":
    thrr = False
  else:
    print("Unknown command: %s"%cmnd)
thr1.join()
thr2.join()


inps = []
# for item in parg:
#   args = pars.parse_args(item)
#   inps = numpy.append(inps,[getattr(args,"d"),getattr(args,"theta"),getattr(args,"a")])
# inps = numpy.reshape(inps, (-1,3))
# inps[:,1] = inps[:,1]/180*numpy.pi

# outs = inps[:,0]*numpy.tan(inps[:,1])+inps[:,2]/2


# .rglob() produces a generator too
# desktop.rglob("*.pdf")

# Which you can wrap in a list() constructor to materialize
print(mgdb.list_collection_names())
  # cat1 = item.parts[3] if len(item.parts)>3 else ""
  # cat2 = item.parts[4] if len(item.parts)>4 else ""
  # cat3 = item.parts[5] if len(item.parts)>5 else ""
  # if len(item.parts)>6:
  #   print(item.absolute())
  # if not item.is_reserved and item.is_file and item.suffix == ".pdf":
  #   print(proj, cat1, cat2, cat3)
  # item.is_file
  # print(list(item.parents)[-3].split("\\")[-1])


# out0 = []
# inp0 = []
# for item in parg:
#   args = pars.parse_args(item)
#   inp0.append(getattr(args,"gamma"))
# out0 = numpy.power(10,numpy.asarray(inp0)/20) if "--db" in sys.argv else numpy.asarray(inp0)
# out0 = (1+out0)/(1-out0)

# output
# tabl = prettytable.PrettyTable()
# tabl.set_style(prettytable.MARKDOWN)
# tabl.align = "l"
# tabl.field_names = ["Kayıt Türü", "Proje/Çalışma", "Kayıt Adı"]
# cunt = 0
# for i, item in enumerate(outs):
#   tabl.add_row(["%s"%(item["ptrn"]),
#                 "%s"%(item["proj"]),
#                 "%s"%(item["name"]),
#                 ])
#   cunt += 1
#   if cunt%os.get_terminal_size().lines == os.get_terminal_size().lines-4:
#     print("\n%s"%tabl)
#     input("Press any key to continue ...")
#     tabl.clear_rows()
#     cunt = 0
#   elif i == len(outs)-1:
#     print("\n%s"%tabl)
# tabl.field_names = ["Kayıt Türü", "Kayıt Adı", "Proje/Çalışma", "Kategoriler", "Büyüklük", "Oluşturma", "Değişim", "Son Erişim"]
# for item in outs:
#   size = ""
#   if item["size"] < 1024:
#       size = f"{item["size"]} bytes"
#   elif item["size"] < pow(1024,2):
#       size = f"{round(item["size"]/1024, 2)} KB"
#   elif item["size"] < pow(1024,3):
#       size = f"{round(item["size"]/(pow(1024,2)), 2)} MB"
#   elif item["size"] < pow(1024,4):
#       size = f"{round(item["size"]/(pow(1024,3)), 2)} GB"
#   tabl.add_row(["%s"%(item["ptrn"]),
#                 "%s"%(item["name"][:25] + (item["name"][15:] and '...')),
#                 "%s"%(item["proj"][:25] + (item["proj"][15:] and '...')),
#                 # "%s"%(item["cats"][:25] + (item["cats"][15:] and '...')),
#                 "%s"%("\n".join([astr[:25]+(astr[15:] and '...') for astr in item["cats"].split(":")])),
#                 "%s"%(size),
#                 "%s"%(datetime.datetime.fromtimestamp(item["ctme"], tz=datetime.timezone(datetime.timedelta(hours=3))).strftime("%Y/%m/%d %H:%M:%S %Z")),
#                 "%s"%(datetime.datetime.fromtimestamp(item["mtme"], tz=datetime.timezone(datetime.timedelta(hours=3))).strftime("%Y/%m/%d %H:%M:%S %Z")),
#                 "%s"%(datetime.datetime.fromtimestamp(item["atme"], tz=datetime.timezone(datetime.timedelta(hours=3))).strftime("%Y/%m/%d %H:%M:%S %Z")),
#                 ])
  
# print("\n%s"%tabl)

