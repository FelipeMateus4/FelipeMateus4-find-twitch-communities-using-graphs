import networkx as netx
import pandas as pds
import community
import matplotlib.pyplot as plot
import os

def ler_grafo(csv_file_edges, csv_file_attributes):
    # Leitura do CSV de arestas
    arestas = pds.read_csv(csv_file_edges)

    # Print os nomes das colunas para depuração
    print("Nomes das colunas em arestas:", arestas.columns)

    # Verifica se a coluna 'from' está presente no DataFrame
    source_column = 'from' if 'from' in arestas.columns else 'Unnamed: 0'

    grafo = netx.from_pandas_edgelist(arestas, source= source_column, target='to')

    # Leitura do CSV de atributos
    atributos = pds.read_csv(csv_file_attributes)


    # Adicionar atributos aos nós no grafo
    for _, attr_row in atributos.iterrows():
        new_id = attr_row['new_id']

        if new_id in grafo.nodes:
            grafo.nodes[new_id].update(attr_row.to_dict())

    return grafo

def louvain_algorithm(grafo):
    partition = community.best_partition(grafo)
    comunidade = {}
    for node, comunidade_id in partition.items():
        if comunidade_id not in comunidade:
            comunidade[comunidade_id] = set()
        comunidade[comunidade_id].add(node)

    # Identificador
    for i, nodes in enumerate(comunidade.values()):
        netx.set_node_attributes(grafo, {node: i for node in nodes}, name=f'comunidade_id')

    # Modularidade
    modularidade = community.modularity(partition, grafo)

    return list(comunidade.values()), modularidade

def identificar_comunidades_hubs(grafo):
    # Identificar hubs
    degree_centrality = netx.degree_centrality(grafo)
    hubs = [node for node, centrality in degree_centrality.items() if centrality >= 0.3]  # Ajuste o limite conforme necessário

    return hubs

def plotar_comunidades(G, comunidade, pontes):
    num_comunidade = len(comunidade) + 1  # Adiciona 1 para as pontes
    num_rows = 2
    num_cols = (num_comunidade + 1) // num_rows

    plot.figure(figsize=(15, 10))

    # Plotar comunidades
    for i, comunidade in enumerate(comunidade, start=1):
        plot.subplot(num_rows, num_cols, i)
        comunidade_grafo = G.subgraph(comunidade)
        pos = netx.spring_layout(comunidade_grafo)
        netx.draw(comunidade_grafo, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=600)
        plot.title(f'Comunidade {i}')

    # Plotar pontes
    plot.subplot(num_rows, num_cols, num_comunidade)
    pontes = G.subgraph(pontes)
    pos_pontes = netx.spectral_layout(pontes)
    netx.draw(pontes, pos_pontes, with_labels=True, font_weight='bold', node_color='salmon', node_size=600)
    plot.title('Pontes entre Comunidades')


    plot.savefig('grafo.png')  # Salvar o gráfico como uma imagem

def analyze_comunidade_content(grafo, comunidade_id):
    comunidade = [node for node, comm_id in netx.get_node_attributes(grafo, 'comunidade_id').items() if comm_id == comunidade_id]

    if not comunidade:
        print(f"Comunidade {comunidade_id} não encontrada.")
        return

    with open('resultados.txt', 'a') as saida_arquivo:  # 'a' para abrir o arquivo em modo de anexo
        saida_arquivo.write(f"Comunidade {comunidade_id}:\n")
        for node in comunidade:
            saida_arquivo.write(f"Node {node}: {grafo.nodes[node]}\n")
        saida_arquivo.write("\n")  # Adicione uma linha em branco entre as comunidades
        
def identifica_pontes_comunidades(grafo, comunidades):
    pontes = netx.bridges(grafo)
    pontes_comunidades = []
    
    for ponte in pontes:
        node, node2 = ponte
        
        # Verifica a qual comunidade cada nó da ponte pertence
        comunidade_node = next((i for i, comm in enumerate(comunidades) if node in comm), None)
        comunidade_node2 = next((i for i, comm in enumerate(comunidades) if node2 in comm), None)

        # Se os IDs de comunidade dos nós forem diferentes, é uma ponte entre comunidades
        if comunidade_node is not None and comunidade_node2 is not None and comunidade_node != comunidade_node2:
            pontes_comunidades.append(ponte)
        
    
    return pontes_comunidades

def main(csv_file_edges_path, csv_file_attributes_path):
    grafo = ler_grafo(csv_file_edges_path, csv_file_attributes_path)

    result_comunidade, modularidade = louvain_algorithm(grafo)

    hubs = identificar_comunidades_hubs(grafo)
    
    pontes_comunidades = identifica_pontes_comunidades(grafo, result_comunidade)
    
    plotar_comunidades(grafo, result_comunidade, pontes_comunidades)
    

    # Substituir o arquivo o arquivo caso ja exista
    if os.path.exists('resultados.txt'):
        os.remove('resultados.txt')
    
    # Abra o arquivo em modo de anexo
    with open('resultados.txt', 'a') as saida_arquivo:
        # Escrever as informações gerais no arquivo
        saida_arquivo.write("Modularidade: {}\n".format(modularidade))
        saida_arquivo.write("Hubs identificados: {}\n".format(hubs))
        saida_arquivo.write("Pontes entre comunidades:{}\n".format(pontes_comunidades))
        saida_arquivo.write("\n") 

        # Escrever informações de cada comunidade
        for i, comunidade in enumerate(result_comunidade, start=1):
            saida_arquivo.write(f"Comunidade {i}:\n")
            for node in comunidade:
                saida_arquivo.write(f"Node {node}: {grafo.nodes[node]}\n")
            saida_arquivo.write("\n")  # Adicione uma linha em branco entre as comunidades
            
    print(f"ndaouidhjaioduhasuiodhjauiosdhasuiodhas")\


if __name__ == "__main__":
    # aviso
    print("por favor execute a funcao principal!")