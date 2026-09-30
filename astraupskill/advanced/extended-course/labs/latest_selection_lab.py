"""Execute extracted real grouping/selection source with explicit domain stand-ins."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
FILES = [ROOT / "jellyfin/Emby.Server.Implementations/Library/UserViewManager.cs", ROOT / "jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs"]

def block(source, signature):
    if source.count(signature) != 1: raise RuntimeError("Source signature changed; review extraction")
    begin = source.index(signature)
    opening = source.index("{", begin)
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == "{": depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0: return source[begin:index + 1]
    raise RuntimeError("Unclosed source block")

def replace_once(text, old, new):
    if text.count(old) != 1: raise RuntimeError("Mutation expression changed; review source")
    return text.replace(old, new)

STUBS = r'''
using System;
using System.Collections.Generic;
using System.Linq;
class BaseItem { public Guid Id { get; set; } public bool IsFolder { get; set; } public BaseItem LatestItemsIndexContainer { get; set; } }
class MusicAlbum : BaseItem { }
class DtoOptions { }
class LatestItemsQuery { public object User { get; set; } public bool GroupItems { get; set; } public int? Limit { get; set; } }
class BaseItemDto { public Guid Id { get; set; } public int ChildCount { get; set; } }
class GroupingHost {
    public IReadOnlyList<BaseItem> Candidates { get; set; } = Array.Empty<BaseItem>();
    private IReadOnlyList<BaseItem> GetItemsForLatestItems(object user, LatestItemsQuery request, DtoOptions options) => Candidates;
'''
HARNESS = r'''
static class Program {
    static int passed;
    static string current = "initialization";
    static void Check(string name, bool value) { current = name; if (!value) throw new Exception("Prediction disagreed"); passed++; }
    static BaseItem Item(BaseItem parent = null, bool folder = false) => new BaseItem { Id = Guid.NewGuid(), LatestItemsIndexContainer = parent, IsFolder = folder };
    static List<Tuple<BaseItem,List<BaseItem>>> Group(BaseItem[] candidates, int limit, bool grouped = true) => new GroupingHost { Candidates = candidates }.GetLatestItems(new LatestItemsQuery { GroupItems = grouped, Limit = limit }, new DtoOptions());
    static Tuple<BaseItem,List<BaseItem>> Pair(BaseItem parent, params BaseItem[] children) => new(parent, children.ToList());
    static int Main() {
        try {
            var a = Item(); var b = Item(); var a1 = Item(a); var a2 = Item(a); var b1 = Item(b);
            Check("empty candidates", Group(Array.Empty<BaseItem>(),2).Count == 0);
            var ungrouped = Group(new[] {a1,a2},5,false);
            Check("ungrouped cardinality", ungrouped.Count == 2);
            Check("ungrouped null containers", ungrouped.All(x => x.Item1 is null));
            var folder = Item(a,true);
            Check("folder bypasses grouping", Group(new[] {folder},2)[0].Item1 is null);
            var sameId = Item(); sameId.Id = a.Id;
            var merged = Group(new[] {a1,Item(sameId)},3);
            Check("container identity groups", merged.Count == 1);
            Check("container identity child count", merged[0].Item2.Count == 2);
            Check("first container object retained", ReferenceEquals(merged[0].Item1,a));
            var early = Group(new[] {a1,b1,a2},2);
            Check("early group bound", early.Count == 2);
            Check("later sibling excluded after threshold", early[0].Item2.Count == 1);
            var one = Group(new[] {a1,a2,b1},1);
            Check("one group bound", one.Count == 1);
            Check("one group stops immediately", one[0].Item2.Count == 1);
            Check("sibling before threshold included", Group(new[] {a1,a2,b1},2)[0].Item2.Count == 2);
            Check("null containers remain separate", Group(new[] {Item(),Item()},3).Count == 2);
            var album = new MusicAlbum { Id = Guid.NewGuid() }; var song = Item(album); var plain = Item();
            var groups = new List<Tuple<BaseItem,List<BaseItem>>> { Pair(a,a1,a2),Pair(b,b1),Pair(album,song),Pair(null,plain) };
            var selected = SelectionHost.Select(groups);
            Check("representative identities", selected.items.Select(x => x.Id).SequenceEqual(new[] {a.Id,b1.Id,album.Id,plain.Id}));
            Check("selected count vector", selected.counts.SequenceEqual(new[] {2,0,1,0}));
            var dtos = selected.items.Select(x => new BaseItemDto { Id=x.Id,ChildCount=99 }).ToList();
            SelectionHost.Restore(dtos,selected.counts);
            Check("mapping identities unchanged", dtos.Select(x=>x.Id).SequenceEqual(selected.items.Select(x=>x.Id)));
            Check("multi-child count restored", dtos[0].ChildCount==2);
            Check("zero leaves mapper value", dtos[1].ChildCount==99);
            Check("singleton album count restored", dtos[2].ChildCount==1);
            Check("null container leaves mapper value", dtos[3].ChildCount==99);
            Check("empty selection", SelectionHost.Select(new()).items.Length==0);
            current="empty child list contract";
            try { SelectionHost.Select(new() { Pair(a) }); throw new Exception("Expected empty-child rejection"); }
            catch (ArgumentOutOfRangeException) { passed++; }
            Console.WriteLine($"PASS {passed} extracted-source algorithm assertions; media types and retrieval are stand-ins; no server or repository execution");
            return 0;
        } catch(Exception error) { Console.Error.WriteLine($"FAIL {current}: {error.GetType().Name}: {error.Message}"); return 1; }
    }
}
'''

def run(command, work):
    result = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=120)
    if result.stdout.strip(): print(result.stdout.strip())
    if result.stderr.strip(): print(result.stderr.strip(), file=sys.stderr)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline","broken-early-break","broken-album","broken-zero-restore"], default="baseline")
    args=parser.parse_args()
    before={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in FILES}
    view,controller=[f.read_text(encoding="utf-8-sig") for f in FILES]
    grouping=block(view,"public List<Tuple<BaseItem, List<BaseItem>>> GetLatestItems(")
    action=block(controller,"public ActionResult<IEnumerable<BaseItemDto>> GetLatestMedia(")
    start=action.index("var resolvedItems =")
    end=action.index("// Fetch DTOs",start)
    selection=action[start:end]
    restore=block(action,"for (int i = 0; i < dtos.Count; i++)")
    if args.mode=="broken-early-break": grouping=replace_once(grouping,"list.Count >= request.Limit","list.Count > request.Limit")
    if args.mode=="broken-album": selection=replace_once(selection,"tuple.Item2.Count > 1 || tuple.Item1 is MusicAlbum","tuple.Item2.Count > 1")
    if args.mode=="broken-zero-restore": restore=replace_once(restore,"childCounts[i] > 0","childCounts[i] >= 0")
    program=STUBS+grouping+"\n}\nstatic class SelectionHost { public static (BaseItem[] items,int[] counts) Select(List<Tuple<BaseItem,List<BaseItem>>> list) {\n"+selection+"return (resolvedItems,childCounts); }\npublic static void Restore(IReadOnlyList<BaseItemDto> dtos,int[] childCounts) {\n"+restore+"\n}\n}\n"+HARNESS
    try:
        with tempfile.TemporaryDirectory(prefix="jellyfin-selection-course-") as folder:
            work=Path(folder).resolve()
            if work.parent != Path(tempfile.gettempdir()).resolve() or not work.name.startswith("jellyfin-selection-course-"): raise RuntimeError("Unexpected owned temporary directory")
            (work/"Program.cs").write_text(program,encoding="utf-8")
            (work/"SelectionLab.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>disable</Nullable></PropertyGroup></Project>',encoding="utf-8")
            (work/"NuGet.Config").write_text('<configuration><packageSources><clear /></packageSources></configuration>',encoding="utf-8")
            if run(["dotnet","restore","SelectionLab.csproj","--configfile","NuGet.Config","--verbosity","quiet"],work).returncode: raise RuntimeError("SDK restore failed; no semantic result")
            if run(["dotnet","build","SelectionLab.csproj","--no-restore","--configuration","Release","--verbosity","quiet"],work).returncode: raise RuntimeError("Build failed; no semantic result")
            result=run(["dotnet",str(work/"bin/Release/net10.0/SelectionLab.dll")],work)
            print("Mode:",args.mode,"semantic exit:",result.returncode)
            return result.returncode
    finally:
        after={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in FILES}
        if after!=before: raise RuntimeError("Original source changed during lab")
        print("Original hashes unchanged:",len(FILES),"source files")

if __name__=="__main__": sys.exit(main())
