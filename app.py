import os
import shlex
import argparse
from TabManager import TabManager
from Theory import get_harmonic_field, get_chord_details, NOTES, CHORD_DATA

# ==========================================
# GUITAR JAZZ HELPER (TEORIA E BRAÇO)
# ==========================================

def display_fretboard(active_notes, root_note, num_frets=12):
    print(f"\n{' '*7}MAPA NO BRAÇO")
    header = "       " + "".join([f"{f:^5}" for f in range(num_frets + 1)])
    print(header)
    print("       " + "-----" * (num_frets + 1))
    for i, start_note in enumerate(['E', 'B', 'G', 'D', 'A', 'E']):
        line = f"{i+1}ª({start_note:^1}) |"
        curr_idx = NOTES.index(start_note)
        for fret in range(num_frets + 1):
            note = NOTES[(curr_idx + fret) % 12]
            if note in active_notes:
                cell = f"[{note}]" if note == root_note else f"({note})"
                line += f"{cell:^5}"
            else: line += f"{'--':^5}"
        print(line)

def run_jazz_helper():
    while True:
        print(f"\n{'='*30}\n GUITAR JAZZ HELPER\n{'='*30}")
        print("[1] Analisar Acorde (Notas + Teoria)\n[2] Filtrar Nota Específica\n[3] Ver Campo Harmônico (7as)\n[0] Voltar ao Menu Principal")
        op = input("\nEscolha: ")

        if op == "0": break
        if op == "1":
            root = input("Fundamental (ex: C): ").upper()
            ctype = input(f"Tipo {list(CHORD_DATA.keys())}: ").lower()
            analysis = get_chord_details(root, ctype)
            if analysis:
                print(f"\n--- Estrutura: {root} {ctype} ---")
                for n, l in analysis.items(): print(f" {n:<4} -> {l}")
                display_fretboard(list(analysis.keys()), root)
            else:
                print("Acorde não encontrado.")
        elif op == "2":
            nota = input("Nota (ex: C, C#): ").upper()
            if nota in NOTES: display_fretboard([nota], nota)
            else: print("Nota inválida.")
        elif op == "3":
            tonalidade = input("Tonalidade (ex: G): ").upper()
            field = get_harmonic_field(tonalidade)
            if field:
                print(f"\n--- CAMPO HARMÔNICO DE {tonalidade} MAIOR ---")
                for chord in field: print(f" {chord}")
                print("-" * 35 + "\n Dica: No Jazz, foque nos graus II, V e I.")
            else: print("Tonalidade inválida.")

# ==========================================
# TM-GUITAR TAB MANAGER (TABLATURAS)
# ==========================================

def show_detailed_help():
    print("""
    ================= DOCUMENTAÇÃO TM-GUITAR =================
    
    GERENCIAMENTO DE PROJETO:
    rename "Nome"       Altera o nome da música atual.
    list                Lista todas as músicas (.tmjazz) na pasta.
    save                Salva o progresso atual em um arquivo .tmjazz.
    load "arquivo"      Carrega uma música existente para edição.
    
    TABLATURA:
    add tab             Adiciona uma faixa (bloco) de 16 colunas.
    render              Exibe a tablatura completa na tela.
    
    EDIÇÃO DE NOTAS E ACORDES:
    set --f --c --pos   Insere uma nota. Ex: set --f 1 --c 4 --pos 5:7
                        Tags:
                        --f    : Faixa (índice do bloco, ex: 1)
                        --c    : Coluna (posição horizontal na faixa, ex: 4)
                        --pos  : Corda:Casa (Corda física e casa no braço, ex: 5:7)
                        
    rem --f --c --s     Remove nota. Ex: rem --f 1 --c 4 --s 5
                        Tags:
                        --f    : Faixa
                        --c    : Coluna
                        --s    : String/Corda de 1 a 6 a ser removida
                        
    CARIMBAR ACORDE:
    set --f 1 --c 1 --chord C:maj7
                        Tags:
                        --f    : Faixa
                        --c    : Coluna
                        --chord: Tônica:Tipo (ex: C:maj7, G:m7)
                                 Utiliza Voicing de Jazz: prioriza tônica na 
                                 5ª ou 6ª corda e deixa a 1ª livre (-).

    del --f [n]         Remove uma faixa inteira de tablatura.
    clear --f [n] --c [n] Limpa todas as notas de uma coluna específica.

    exit                Volta ao menu principal.
    ==========================================================
    """)

def list_musics():
    folder = "compositions"
    if not os.path.exists(folder):
        print("Nenhuma pasta de composições encontrada.")
        return
    files = [f for f in os.listdir(folder) if f.endswith(".tmjazz")]
    if not files:
        print("Nenhuma música (.tmjazz) encontrada.")
    else:
        print("\n--- ARQUIVOS DISPONÍVEIS ---")
        for f in files: print(f"  > {f}")

class NoExitParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

def run_tab_manager():
    manager = TabManager("Nova Musica")
    
    set_parser = NoExitParser(add_help=False)
    set_parser.add_argument("--f", type=int)
    set_parser.add_argument("--c", type=int)
    set_parser.add_argument("--pos", type=str)
    set_parser.add_argument("--chord", type=str)

    rem_parser = NoExitParser(add_help=False)
    rem_parser.add_argument("--f", type=int)
    rem_parser.add_argument("--c", type=int)
    rem_parser.add_argument("--s", type=int)
    
    clear_parser = NoExitParser(add_help=False)
    clear_parser.add_argument("--f", type=int)
    clear_parser.add_argument("--c", type=int)

    print("\nIniciando TM-Guitar... Digite 'help' para comandos ou 'exit' para voltar.")

    while True:
        try:
            line = input(f"\n[TM: {manager.name}] > ")
            if not line: continue
            
            parts = shlex.split(line)
            cmd = parts[0]
            args = parts[1:]

            if cmd == "exit": break
            elif cmd == "help": show_detailed_help()
            elif cmd == "list": list_musics()
            elif cmd == "render": manager.render()
            
            elif cmd == "clear":
                try:
                    p = clear_parser.parse_args(args)
                    print(manager.clear_column(p.f, p.c))
                    manager.render()
                except:
                    print("Uso: clear --f [n] --c [n]")

            elif cmd == "del" and "--f" in args:
                try:
                    f_val = args[args.index("--f") + 1]
                    print(manager.delete_tab(f_val))
                    manager.render()
                except:
                    print("Uso: del --f [n]")
            
            elif cmd == "rename":
                if args: print(manager.rename(args[0]))
                else: print("Uso: rename \"Novo Nome\"")

            elif cmd == "save":
                print(manager.save_json())

            elif cmd == "load":
                if args:
                    new_manager, msg = TabManager.load_json(args[0])
                    if new_manager:
                        manager = new_manager
                        manager.render()
                    print(msg)
                else: print("Uso: load nome_do_arquivo.tmjazz")

            elif cmd == "add" and "tab" in args:
                print(manager.add_tab())
                manager.render()

            elif cmd == "set":
                try:
                    p = set_parser.parse_args(args)
                    if p.chord:
                        print(manager.set_chord_auto(p.f, p.c, p.chord))
                    elif p.pos:
                        print(manager.set_pos(p.f, p.c, p.pos))
                    manager.render()
                except:
                    print("Erro: Use set --f 1 --c 1 --pos 6:3 OU --chord C:maj7")

            elif cmd == "rem":
                try:
                    p = rem_parser.parse_args(args)
                    print(manager.remove_pos(p.f, p.c, p.s))
                    manager.render()
                except:
                    print("Uso: rem --f [n] --c [n] --s [n]")
            else:
                print("Comando desconhecido. Digite 'help' para ajuda.")
            
        except Exception as e:
            print(f"Erro: Verifique os parâmetros ou use 'help'. Detalhe: {e}")

# ==========================================
# MENU PRINCIPAL
# ==========================================

def main():
    while True:
        print(f"\n{'='*40}")
        print(f" CLI MUSIC STUDIO - MENU PRINCIPAL")
        print(f"{'='*40}")
        print("[1] TM-Guitar Tab Manager (Montar Tablatura)")
        print("[2] Guitar Jazz Helper (Teoria e Braço)")
        print("[0] Sair do Sistema")
        
        op = input("\nEscolha uma opção: ")

        if op == "0": 
            print("Saindo do CLI Music...")
            break
        elif op == "1":
            run_tab_manager()
        elif op == "2":
            run_jazz_helper()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaindo...")
