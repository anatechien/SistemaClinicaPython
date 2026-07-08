class PagamentoForaDoPrazoException(Exception):
  def __init__(self, data_pagamento: str, data_atendimento: str):
    super().__init__(
      f"Pagamento deve ser realizado até a data do atendimento "
      f"({data_atendimento}). Data informada: {data_pagamento}."
    )
