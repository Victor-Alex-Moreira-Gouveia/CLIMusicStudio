from Theory import get_chord_notes, NOTES
import json
import os

class TabManager:
    def __init__(self, music_name="Sem Titulo"):
        self.name = music_name
        self.tabs = []
        self.cols_per_tab = 16
        self.string_map = {"1":"E", "2":"B", "3":"G", "4":"D", "5":"A", "6":"E_low"}
        self.folder = "compositions"
        
        # Garante que a pasta de composições existe
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def add_tab(self):
        """
        Cria uma nova faixa vazia de 6 cordas e 16 colunas.
        Adiciona a faixa à lista de tablaturas do projeto.
        """
        new_tab = {k: ["-"] * self.cols_per_tab for k in self.string_map.values()}
        self.tabs.append(new_tab)
        return f"-> Faixa {len(self.tabs)} criada com sucesso."
    
    def rename(self, new_name):
        """Altera o nome da música na memória."""
        old_name = self.name
        self.name = new_name
        return f"Projeto renomeado de '{old_name}' para '{new_name}'."
    
    def set_pos(self, faixa, coluna, pos):
        try:
            f_idx, c_idx = int(faixa)-1, int(coluna)-1
            corda, casa = pos.split(":")
            target = self.string_map.get(corda)
            
            if f_idx >= len(self.tabs): return "Erro: Faixa inexistente. Use 'add tab'."
            
            self.tabs[f_idx][target][c_idx] = casa
            return f"Sucesso: Corda {corda} alterada para casa {casa}."
        except Exception as e:
            return f"Erro no comando: {e}"

    def remove_pos(self, faixa, coluna, corda):
        try:
            f_idx, c_idx = int(faixa)-1, int(coluna)-1
            target = self.string_map.get(str(corda))
            self.tabs[f_idx][target][c_idx] = "-"
            return "Nota removida."
        except: return "Erro nas coordenadas."

    def set_chord_auto(self, faixa, coluna, chord_str):
        """
        Carimba um acorde automaticamente em uma coluna, utilizando lógica de 'Voicing de Jazz'.
        Prioriza a nota tônica na 5ª ou 6ª corda, e deixa a 1ª corda livre para melodias 
        (apagando-a com '-').
        """
        try:
            # 1. LIMPEZA TOTAL DA COLUNA PRIMEIRO
            self.clear_column(faixa, coluna)
            
            root, ctype = chord_str.split(":")
            notas_alvo = get_chord_notes(root, ctype)
            tonica = root.upper()
            
            f_idx, c_idx = int(faixa)-1, int(coluna)-1
            # Focaremos nas cordas 6, 4, 3, 2 (Comum no Jazz para Shell Voicings)
            # Ou 5, 4, 3, 2.
            tuning_notes = ['E', 'B', 'G', 'D', 'A', 'E']
            string_keys = ["E", "B", "G", "D", "A", "E_low"]
            
            # Notas que o carimbo vai tentar preencher (evitando a 1ª corda por padrão no Jazz)
            target_strings = ["E_low", "A", "D", "G", "B"]

            for i, start_note in enumerate(tuning_notes):
                current_key = string_keys[i]
                if current_key not in target_strings:
                    continue # Pula a 1ª corda (E aguda) para manter o voicing limpo

                current_idx = NOTES.index(start_note)
                found = False
                
                # Prioriza Tônica no baixo
                if current_key in ["E_low", "A"]:
                    for casa in range(6):
                        if NOTES[(current_idx + casa) % 12] == tonica:
                            self.tabs[f_idx][current_key][c_idx] = str(casa)
                            found = True
                            break
                
                if not found:
                    for casa in range(6):
                        if NOTES[(current_idx + casa) % 12] in notas_alvo:
                            self.tabs[f_idx][current_key][c_idx] = str(casa)
                            break
            
            return f"Acorde {chord_str} carimbado (Voicing de Jazz)."
        except:
            return "Erro no carimbo automático."

    @classmethod
    def load_json(cls, filename):
        """Carrega um arquivo .tmjazz da pasta de composições."""
        folder = "compositions"
        # Garante que a extensão esteja lá
        if not filename.endswith(".tmjazz"):
            filename += ".tmjazz"
            
        path = os.path.join(folder, filename)
        
        if not os.path.exists(path):
            return None, f"Erro: O arquivo '{filename}' não foi encontrado em /{folder}."

        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            if data.get("tm_version") != "1.0":
                return None, "Erro: Este arquivo não é um formato .tmjazz válido."

            instance = cls(data["name"])
            instance.tabs = data["tabs"]
            instance.cols_per_tab = data.get("cols", 16)
            return instance, f"Música '{data['name']}' carregada!"
        except Exception as e:
            return None, f"Erro ao ler arquivo: {e}"

    def save_json(self):
        filename = f"{self.name.lower().replace(' ', '_')}.tmjazz"
        path = os.path.join(self.folder, filename)
        
        data = {
            "tm_version": "1.0",  # Nossa "assinatura"
            "name": self.name,
            "tabs": self.tabs,
            "cols": self.cols_per_tab
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Música salva em: {path}"

    def render(self):
        if not self.tabs:
            print(f"\n--- {self.name} (Vazio) ---")
            return
        
        keys = ["E", "B", "G", "D", "A", "E_low"]
        labels = ["1ª(E)", "2ª(B)", "3ª(G)", "4ª(D)", "5ª(A)", "6ª(E)"]
        print(f"\n--- {self.name} ---")
        for i, tab in enumerate(self.tabs):
            print(f"\n[ FAIXA {i+1} ]")
            header = "       " + "".join([f"{c:<3}" for c in range(1, self.cols_per_tab + 1)])
            print(header)
            for idx, key in enumerate(keys):
                line = "  ".join(tab[key])
                print(f"{labels[idx]} | {line} |")

    def clear_column(self, faixa, coluna):
        """
        Reseta todas as 6 cordas de uma coluna específica, inserindo '-'.
        Útil para limpar a coluna antes de adicionar notas ou acordes.
        """
        try:
            f_idx = int(faixa) - 1
            c_idx = int(coluna) - 1
            
            if f_idx >= len(self.tabs):
                return "Erro: Faixa não existe."
            
            for string_key in self.string_map.values():
                self.tabs[f_idx][string_key][c_idx] = "-"
            
            return f"Coluna {coluna} da Faixa {faixa} foi limpa."
        except Exception as e:
            return f"Erro ao limpar coluna: {e}"

    def delete_tab(self, faixa):
        """
        Remove uma faixa inteira de tablatura do projeto baseando-se no índice informado.
        """
        try:
            f_idx = int(faixa) - 1
            if 0 <= f_idx < len(self.tabs):
                self.tabs.pop(f_idx)
                return f"Faixa {faixa} removida com sucesso."
            return f"Erro: A Faixa {faixa} não foi encontrada."
        except:
            return "Erro: Informe um número de faixa válido."