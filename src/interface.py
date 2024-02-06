import tkinter as tk
from tkinter import filedialog
import cv2
import os
from PIL import Image, ImageTk
import r1
from tkinter import Text
import threading

class interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Twitch_grafos")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        self.master.geometry(f"{screen_width}x{screen_height}")

        diretorio = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(diretorio, "background.mp4")

        self.cap = cv2.VideoCapture(video_path)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        
        self.canvas = tk.Canvas(self.master, width=screen_width, height=screen_height)
        self.canvas.pack()
        # crua uma thread separada para rodar o video da interface
        self.video_thread = threading.Thread(target=self.play_video)
        self.video_thread.daemon = True
        self.video_thread.start()
        # ficou um pouco extenso a texto dos botoes. No geral o codigo deles é o mesmo, o que muda é a string do botao e a posicao no eixo y
        # botao dos dados
        botao_arquivos = tk.Button(self.master, text="ver os dados encontrados", command=self.dados_natela, width=20, height=2, font=("Arial", 14), bg="black", fg="white")
        botao_arquivos.place(relx=0.07, rely=0.4, anchor=tk.CENTER)
        # botao dos arquivos
        botao_dados = tk.Button(self.master, text="Selecionar os arquivos \n (edges,target)", command=self.selecionar_arquivos, width=20, height=2, font=("Arial", 14), bg="black", fg="white")
        botao_dados.place(relx=0.07, rely=0.3, anchor=tk.CENTER)
        # botao de visualizacao
        botao_visualizador = tk.Button(self.master, text="Visualizar grafo de \n comunidades", command=self.visualizar_imagem, width=20, height=2, font=("Arial", 14), bg="black", fg="white")
        botao_visualizador.place(relx=0.07, rely=0.5, anchor=tk.CENTER)
        # botao para sair
        botao_sair = tk.Button(self.master, text="Sair", command=self.close_interface, width=20, height=2, font=("Arial", 14), bg="black", fg="white")
        botao_sair.place(relx=0.07, rely=0.6, anchor=tk.CENTER)
        
        # Lidar com o evento de fechamento da janela principal
        self.master.protocol("WM_DELETE_WINDOW", self.close_interface)
    
    def visualizar_imagem(self):
        imagem = Image.open("grafo.png")
                            
        imagem_tam = (1366, 720) # Tamanho da imagem
        
        imagem_nova = imagem.resize(imagem_tam, resample = Image.LANCZOS) # ajustes do tamanho da imagem
        
        janela = tk.Toplevel(self.master)
        janela.title("visualizar imagem")
        
        imagem_label = tk.Label(janela, image=None)  
        imagem_label.image = ImageTk.PhotoImage(imagem_nova)
        imagem_label.config(image=imagem_label.image)
        imagem_label.pack()
        
        fechar_botao = tk.Button(janela, text="Fechar", command=janela.destroy)
        fechar_botao.pack()

    def selecionar_arquivos(self):
        csv_file_edges_path = filedialog.askopenfilename(title="Selecione o arquivo CSV de arestas", filetypes=[("CSV files", "*.csv")])
        csv_file_attributes_path = filedialog.askopenfilename(title="Selecione o arquivo CSV de atributos", filetypes=[("CSV files", "*.csv")])

        if csv_file_edges_path and csv_file_attributes_path:
            r1.main(csv_file_edges_path, csv_file_attributes_path)

            # Atualize o texto na interface para indicar que as comunidades foram identificadas
            mensagem = tk.Label(self.master, text="Arquivos 'resultados.txt e grafo.png' gerados! FIque a vontade para visualiza-los", font=("Arial", 14), fg="green")
            mensagem.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
            
            self.master.after(5000, mensagem.destroy)
            
            
            
    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            aspect_ratio = frame.shape[1] / frame.shape[0]
            new_height = int(self.master.winfo_screenwidth() / aspect_ratio)
            frame = cv2.resize(frame, (self.master.winfo_screenwidth(), new_height))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=image)

            if hasattr(self, "canvas_image"):
                self.canvas.delete(self.canvas_image)

            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            
            if not ret or cv2.waitKey(30) & 0xFF == ord('q'):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Chame a função play_video novamente após 1 milissegundo
        self.master.after(1, self.play_video)
        
    def dados_natela(self):
        with open("resultados.txt", "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                
                janela_dados = tk.Toplevel(self.master)
                janela_dados.title("Conteúdo das Comunidades")
                
                text_widget = Text(janela_dados, wrap=tk.WORD)
                text_widget.insert(tk.END, conteudo)
                text_widget.pack(expand=True, fill=tk.BOTH)

                voltar_botao = tk.Button(janela_dados, text="Voltar", command=janela_dados.destroy)
                voltar_botao.pack()
                
    def close_interface(self):
        self.master.destroy()  # nunca apagar essas duas linhas
        self.master.quit()  # NUUNNCA


def main():
    root = tk.Tk()
    app = interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()