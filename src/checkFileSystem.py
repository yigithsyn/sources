from pymongo import MongoClient


def chfs(exit=False):
  while not exit:
    for item in mgdb.get_collection("project").find({}):
      path = pathlib.Path("D:/00 PROJELER/").joinpath(item["project"]).joinpath("/".join(item["categories"]),item["name"])
      if not path.exists(follow_symlinks=False):
        print("Path does not exists any more")
        mgdb.get_collection("project").delete_one({"_id": bson.ObjectId(item["_id"])})
      else:
        pass
      if not thrr:
        break