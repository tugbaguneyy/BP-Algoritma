

def create_graph_with_initial_position(initial_pose, trash_positions):
    G = nx.Graph()
    
    # Başlangıç konumunu düğüm olarak ekle
    start_x = initial_pose["pose"]["position"]["x"]
    start_y = initial_pose["pose"]["position"]["y"]
    G.add_node("Start", pos=(start_x, start_y))

    # Çöp noktalarını düğüm olarak ekle
    for i, pos in enumerate(trash_positions):
        G.add_node(f"Trash {i+1}", pos=(pos[0], pos[1]))
    
    # Başlangıç noktasından her çöp noktasına olan mesafeleri hesapla ve kenarları ekle
    for i, pos in enumerate(trash_positions):
        distance = calculate_distance(start_x, start_y, pos[0], pos[1])
        G.add_edge("Start", f"Trash {i+1}", weight=distance)

    # Her çöp noktası çifti için mesafeleri hesapla ve sadece bir kez kenarları ekle
    for i in range(len(trash_positions)):
        for j in range(i+1, len(trash_positions)):
            distance = calculate_distance(trash_positions[i][0], trash_positions[i][1], trash_positions[j][0], trash_positions[j][1])
            if not G.has_edge(f"Trash {i+1}", f"Trash {j+1}"):  # Kenar zaten eklenmemişse ekle
                G.add_edge(f"Trash {i+1}", f"Trash {j+1}", weight=distance)

    return G



import networkx as nx
import matplotlib.pyplot as plt
import time
import random
initial_pose = {
    "pose": {
        "position": {
            "x": 0.036,
            "y": 0.009
        },
        "orientation": {
            "z": -0.010,
            "w": 0.99
        }
    }
}




def calculate_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def draw_graph(graph):
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

# # Örnek kullanım
# trash_positions = [[10, 20, 30], [15, 25, 35]]
# graph = trash_positions_to_graph(trash_positions)
# draw_graph(graph)

def plan_path_with_mst(graph):
    # Verilen graf üzerinde Kruskal algoritmasını kullanarak Minimum Spanning Tree (MST) oluştur
    mst = nx.minimum_spanning_tree(graph)

    # MST'deki kenarları (yolları) alma
    paths = list(mst.edges)

    return paths

def update_initial_pose(visited_nodes, graph):
    if visited_nodes:  # Eğer visited_nodes listesi boş değilse
        last_visited_node = visited_nodes[-1]  # Son ziyaret edilen düğümün adını al
        last_visited_position = graph.nodes[last_visited_node]['pos']  # Son ziyaret edilen düğümün konumunu al
        initial_pose = {  # Yeni initial_pose oluştur
            "pose": {
                "position": {
                    "x": last_visited_position[0],
                    "y": last_visited_position[1]
                },
                "orientation": {
                    "z": -0.010,
                    "w": 0.99
                }
            }
        }
        return initial_pose
    else:  # Eğer visited_nodes listesi boşsa (henüz hiç düğüm ziyaret edilmemişse)
        return None

def main(): 
    # Her indekste üç değişken içeren bir liste oluştur
    trash_positions = []
    #Ziyaret edilen noktaları kaydetmek için:
    visited=[]
    #Hedef çöp pozisyonu
    target_trash_position=(0,0,0)

    #Süre değiştirilebilir
    t=5


    trash_positions.append([ 2.298, -1.38])
    trash_positions.append([3.794, -0.195])
    trash_positions.append([3.094, -0.195])

    # # Listeyi yazdır
    # print("Konumlar:", trash_positions)
    # print("Başlangıç konumu:",initial_pose)
    graph = create_graph_with_initial_position(initial_pose, trash_positions)
    #draw_graph(graph)
    paths = plan_path_with_mst(graph)
    #print("Gidilecek yol:", paths)

    #Gidilecek çöp noktaları için döngü
    for edge in paths:
        for node in edge:
            if node not in visited:
                visited.append(node)
                #visited noktaları sil
                current_position = graph.nodes[node]['pos']
                print("Şu anki konum:", current_position)
                 
                 # Belirli bir süre boyunca döngüyü çalıştır
                start_time = time.time()
                while time.time() - start_time < t:  # t saniye boyunca döngüyü çalıştır
                    #Random olarak 0 ya da 1 üretiyoruz. 0=çöp görmediği durum 1=çöp gördüğü durum
                    if(random.randint(0, 1)):
                        new_point= ((random.uniform(2, 4)),(random.uniform(-0.1,-2)))
                        print("yeni nokta:",new_point)
                        trash_positions.append(new_point)
                        graph = create_graph_with_initial_position(initial_pose, trash_positions)
                        #draw_graph(graph)
                        paths = plan_path_with_mst(graph)
                        print(paths)
                        time.sleep(random.randint(3,5))

                
                time.sleep(2) 
                print("Çöp alındı.")

    print("Tüm noktalar ziyaret edildi.")
  
# Using the special variable  
# __name__ 
if __name__=="__main__":
     main()