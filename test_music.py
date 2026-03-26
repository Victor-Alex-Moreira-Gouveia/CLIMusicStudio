import pytest
import os
import json
from TabManager import TabManager

# --- TESTES DE ESTRUTURA ---

def test_add_tab():
    """Testa se uma nova faixa é criada corretamente com 16 colunas."""
    tm = TabManager("Teste Unitario")
    tm.add_tab()
    assert len(tm.tabs) == 1
    # Verifica se a corda Mi (E) tem 16 espaços
    assert len(tm.tabs[0]["E"]) == 16
    assert tm.tabs[0]["E"][0] == "-"

def test_rename():
    """Testa a função de renomear o projeto."""
    tm = TabManager("Antigo")
    tm.rename("Novo Nome")
    assert tm.name == "Novo Nome"

# --- TESTES DE EDIÇÃO ---

def test_set_pos():
    """Testa a inserção de uma nota individual."""
    tm = TabManager("Teste")
    tm.add_tab()
    # Inserir na Faixa 1, Coluna 5, Corda 6, Casa 3 (Nota Sol)
    tm.set_pos(1, 5, "6:3")
    assert tm.tabs[0]["E_low"][4] == "3" # Indice 4 = Coluna 5

def test_remove_pos():
    """Testa se a remoção volta a nota para '-'."""
    tm = TabManager("Teste")
    tm.add_tab()
    tm.set_pos(1, 1, "1:12")
    tm.remove_pos(1, 1, 1) # Faixa 1, Coluna 1, Corda 1
    assert tm.tabs[0]["E"][0] == "-"

# --- TESTES DE INTELIGÊNCIA MUSICAL (INTEGRAÇÃO) ---

def test_set_chord_auto_cleanup():
    """Garante que o carimbo de acorde limpa a coluna antes de preencher."""
    tm = TabManager("Teste Overwrite")
    tm.add_tab()
    # Coloca nota 12 na 1ª corda (E aguda)
    tm.set_pos(1, 1, "1:12")
    
    # Carimba G:7 (que agora ignora a 1ª corda na nossa lógica de Jazz)
    tm.set_chord_auto(1, 1, "G:7")
    
    # Agora o assert deve passar pois a 1ª corda foi limpa e ignorada pelo carimbo
    assert tm.tabs[0]["E"][0] == "-" 


# --- TESTES DE ARQUIVO (I/O) ---

def test_save_and_load(tmp_path):
    """Testa se o sistema salva e carrega o arquivo .tmjazz corretamente."""
    # Usamos uma pasta temporária do pytest para não sujar sua pasta real
    tm = TabManager("MusicaTeste")
    tm.folder = tmp_path # Redireciona a pasta de save para o temp
    tm.add_tab()
    tm.set_pos(1, 1, "6:3")
    
    # Salva
    tm.save_json()
    
    # Carrega (Precisamos simular o load_json apontando para a pasta temp)
    # Nota: Como o load_json é um @classmethod, ele usa a pasta 'compositions' fixa.
    # Para o teste, vamos verificar apenas se o arquivo existe e o conteúdo é válido.
    filename = os.path.join(tmp_path, "musicateste.tmjazz")
    assert os.path.exists(filename)
    
    with open(filename, 'r') as f:
        data = json.load(f)
        assert data["name"] == "MusicaTeste"
        assert data["tm_version"] == "1.0"

def test_clear_column():
    """Testa se a limpeza de coluna reseta todas as cordas para '-'."""
    tm = TabManager("Teste Limpeza")
    tm.add_tab()
    # Preenche a coluna 1 com várias notas
    tm.set_pos(1, 1, "6:3")
    tm.set_pos(1, 1, "5:2")
    tm.set_pos(1, 1, "4:0")
    
    # Limpa a coluna
    tm.clear_column(1, 1)
    
    # Verifica se todas voltaram ao padrão
    for corda in ["E_low", "A", "D", "G", "B", "E"]:
        assert tm.tabs[0][corda][0] == "-"

def test_delete_tab():
    """Testa a remoção de um bloco inteiro de tablatura."""
    tm = TabManager("Teste Delete")
    tm.add_tab() # Faixa 1
    tm.add_tab() # Faixa 2
    assert len(tm.tabs) == 2
    
    tm.delete_tab(1) # Remove a primeira
    assert len(tm.tabs) == 1
    # A antiga Faixa 2 agora deve ser a única na lista
    assert tm.tabs is not None

def test_set_chord_auto_jazz_voicing():
    """Garante que o carimbo utilza Voicing de Jazz e coloca tônica no baixo adequado."""
    tm = TabManager("Teste Voicing")
    tm.add_tab()
    
    # Acorde C:maj7. Tônica C deve ir pra corda A (casa 3)
    tm.set_chord_auto(1, 1, "C:maj7")
    
    assert tm.tabs[0]["A"][0] == "3"
    assert tm.tabs[0]["E"][0] == "-"