dict={
    "name":"shrey",
    "age":30,
    "sport":"football"
}

# for i,j in dict:
#     print(f"{i}{j}")
    
for key,values in dict.items():
    print(key)
    print(values)
    
    
import pprint

my_nested_dict = {
    "person1": {"name": "Alice", "age": 30},
    "person2": {"name": "Bob", "age": 25, "occupation": "Engineer"}
}
for i in my_nested_dict:
    for j in my_nested_dict[i].values():
        print(j)
        
        