from pymongo   import MongoClient
from pathlib   import Path
from threading import Thread, enumerate
from bson      import ObjectId 
from logging   import getLogger
from logging   import basicConfig as logb
from logging   import INFO        as logi
from flask     import Flask
from atexit    import register

exit = False

logb(level=logi)
logg = getLogger("sources")
logc = {
  "CIFS": "Change In Filesystem"
}

mgcl = MongoClient()
mgdb = mgcl["sources"]
mgcp = mgdb.get_collection("proj")

def chfs():
  global exit
  while not exit:
    for item in mgcp.find({}):
      path = Path("D:/00 PROJELER/").joinpath(item["proj"]).joinpath("/".join(item["cats"]),item["name"])
      if not path.exists(follow_symlinks=False):
        print("Path does not exists any more")
        mgcp.delete_one({"_id": ObjectId(item["_id"])})
      else:
        pass
      if exit:
        break

def updb():
  global  exit
  while not exit:
    ptrn = "PDF Document"
    for item in Path("D:/00 PROJELER/").rglob("*.pdf"):
      stat = item.stat()
      obje = {
        "ptrn": ptrn,
        "name": item.name,
        "proj": item.parts[2],
        "cats": item.parts[3:-1],
        "size": stat.st_size,
        "ctme": 0,
        "mtme": stat.st_mtime,
        "atme": stat.st_atime,
      }
      try:
        obje["ctme"] = stat.st_birthtime
      except:
        obje["ctme"] = stat.st_ctime
      
      fobj = mgcp.find_one({"ptrn":obje["ptrn"], "name":obje["name"], "proj":obje["proj"], "cats":obje["cats"]})
      if fobj:
        if fobj["ctme"] != obje["ctme"] or fobj["mtme"] != obje["mtme"] or fobj["atme"] != obje["atme"]:
          logg.info("%s:%s:%s:%s"%("[Change in Filesystem]",fobj["ptrn"],fobj["proj"],fobj["name"]))
          mgcp.update_one({"_id": ObjectId(fobj["_id"])}, {"$set": {"ctme": obje["ctme"], "mtme": obje["mtme"], "atme": obje["atme"] }})
      else:
        mgcp.insert_one(obje)
      if exit:
        break

thr1 = Thread(target=chfs, name='Check Filesystem')
thr1.daemon = True
thr1.start()

thr2 = Thread(target=updb, name='Update Database')
thr2.daemon = True
thr2.start()

serv = Flask(__name__)

@serv.route('/')
def index():
  return '<h1>Hello World!</h1>'

serv.run(threaded=True, debug=True)

# thr1.join()
# thr2.join()



