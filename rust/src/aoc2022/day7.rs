use rdcl_aoc_helpers::input::WithReadLines;
use std::{fs::File, collections::{HashMap}, cell::RefCell, rc::Rc};

pub fn day7(path: &String) {

    let data:String = File::open(path).read_lines::<String>(1).collect();

    let mut fs = FileSystemTree::new("/", FileType::Directory, None);
    let mut current = fs.to_owned();
    current.add_child("a", FileType::Directory, Some(0));
    current.add_child("b", FileType::Directory, Some(0));
    current.add_child("c", FileType::Directory, Some(0));
    fs = current.to_owned();
    let mut parent = fs;
    let mut son =  parent.children.get("b").unwrap().borrow_mut().to_owned();
    son.add_child("f", FileType::File, Some(1234));
    parent.update_child(son);
    
    
    current = parent;

    
    println!("{}", current);

    println!("Part 1: {}", 0);
    println!("Part 2: {}", 0);
}

/*fn place(rec: &mut FileSystemTree, child: FileSystemTree) {
    rec.children.get_or_insert(child.name.clone(), Box::new(child));
}*/

#[derive(Debug, Clone, PartialEq, Eq)]
struct FileSystemTree {
    name: String,
    children: HashMap<String, Rc<RefCell<FileSystemTree>>>,
    nodetype: FileType,
    size: u32
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum FileType {
    File,
    Directory,
}

impl FileSystemTree {
    fn new(name: &str, nodetype: FileType, size:Option<u32>) -> FileSystemTree {
        FileSystemTree {
            name : name.to_string(),
            children: HashMap::new(),
            nodetype,
            size: size.unwrap_or(0)
        }
    }

    fn size(&self) -> u32 {
        let mut size = self.size;
        for node in self.children.iter() {
            size += node.1.borrow().size;
        }
        size
    }

    fn add_child(&mut self, name: &str, file_type: FileType, size: Option<u32>) {
        if self.nodetype == FileType::File {
            panic!("Cannot add children to a file");
        }

        //let mut children = self.children;
        self.children.insert(name.to_string(), Rc::new(RefCell::new(FileSystemTree::new(name, file_type, size))));
    }

    fn update_child(&mut self, child: FileSystemTree) {
        self.children.insert(child.name.clone(), Rc::new(RefCell::new(child)));
    }

}

impl std::fmt::Display for FileSystemTree {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut r = format!(" {}  {} - {}\n", if self.nodetype == FileType::Directory {"dir  "} else {"file "}, self.name, self.size());
        for node in self.children.iter() {
            let s = node.1.borrow().to_string();
            for line in s.lines() {
                r +=&("-".to_owned() + line + "\n");
            }
        }
        write!(f, "{}", r)
    }
}
