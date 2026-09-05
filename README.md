# 🚛 Truck Queue Simulator

Simulador de fila de recursos para operações portuárias: caminhões chegam
precisando de um tipo específico de equipamento (RTG ou Reach Stacker), e o
sistema aloca automaticamente o equipamento disponível compatível. Quando não
há equipamento livre, o caminhão entra em uma fila de espera (FIFO) e é
atendido automaticamente assim que um equipamento do tipo certo é liberado.

Este projeto nasceu da minha experiência prática como operador de guindaste em
terminal portuário, onde a alocação de equipamentos para atendimento de
caminhões é um processo real do dia a dia. A proposta foi modelar essa lógica
em código, aplicando estruturas de dados e regras de negócio.

## Funcionalidades

- **Alocação automática de equipamento**: busca o primeiro equipamento livre
  e compatível com o tipo necessário pelo caminhão (RTG ou RS).
- **Cálculo automático de horário de saída**: a partir do horário de chegada
  e da duração estimada do atendimento.
- **Fila de espera (FIFO)**: caminhões sem equipamento disponível aguardam;
  quando um equipamento libera, o primeiro caminhão da fila compatível com
  aquele tipo é processado automaticamente.
- **Liberação de equipamento**: simula o equipamento terminando um
  atendimento e ficando disponível novamente.
- **Relatório de estatísticas**: total de caminhões atendidos, em espera,
  soma e média do tempo de atendimento.

## Tecnologias

- **Python** 3 (sem dependências externas)
- **datetime / timedelta** (cálculo de horários, biblioteca padrão)

## Estrutura do projeto

```
simulador-fila-caminhoes/
├── dados.py     # Dados de exemplo: lista de equipamentos e caminhões
├── logica.py     # Regras de negócio: alocação, liberação, fila e relatório
├── main.py         # Executa a simulação completa e imprime os relatórios
└── README.md
```

## Como funciona a lógica (resumo)

1. Cada caminhão tem um tipo de equipamento necessário (`equipment_needed`).
2. `find_available_equipment` procura um equipamento livre desse tipo.
3. Se encontrar, `process_truck` aloca o equipamento e calcula o horário de
   saída do caminhão.
4. Se não encontrar, o caminhão permanece em espera (`departure_time: None`).
5. Quando um equipamento é liberado (`release_equipment`),
   `process_queue_after_release` verifica automaticamente se há algum
   caminhão esperando por aquele tipo e o processa em seguida (FIFO).

## Como rodar

Não precisa instalar nenhuma dependência — só Python 3.

```bash
git clone https://github.com/FabianoSeara/simulador-fila-caminhoes.git
cd simulador-fila-caminhoes
python main.py
```

## Exemplo de saída

```
truck ABC1234 alocated equipment 2 (RTG)
truck AXF 3333 alocated equipment 5 (RS)
truck GHI9012 alocated equipment 3 (RTG)
Truck JKL3456 waiting, no RS available.
Truck DEF5678 waiting, no RTG available.
============================================================
FINAL REPORT
============================================================
served trucks: 3
waiting trucks: 2
total trucks: 5
total duration sum: 75
average service time: 25.0

--- Simulating equipment 2 release ---
Found Truck DEF5678 waiting for RTG
truck DEF5678 alocated equipment 2 (RTG)
...
served trucks: 5
waiting trucks: 0
```

## Próximos passos

- [ ] Simulação em tempo real (relógio avançando minuto a minuto), em vez de
      liberações manuais
- [ ] Geração de dados de teste aleatórios (mais caminhões, mais equipamentos)
- [ ] Exportar relatório final em CSV

---

Projeto desenvolvido por [Fabiano Seára](https://github.com/FabianoSeara) como
parte do meu portfólio de transição de carreira para desenvolvimento de
software, com apoio de IA (Claude) no processo de aprendizado.
