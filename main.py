# Aqui vai ficar o orquestrador das tasks
from datetime import datetime, timezone
from task.landing_extracao_alunos_bubble import ExtracaoDadosBubbleAliunoMentor
from task.landing_extracao_db_bubble import ExtracaoDadosBubbleDiarioBordo
from task.landing_extracao_metas_newgate import ExtracaoApiNewGate
from task.trusted_manipulacao_db_bubble import ManipulationTrustedDbBubble
from task.trusted_manipulacao_metas_newgate import ManipulationTrustedMetasNewgate
from task.trusted_manipulation_user_bubble import ManipulationTrustedUserBubble
from task.business_apply_rule_rt import BusinessApplyRuleRT

import os
import pandas as pd

class Main:
    '''Classe principal para orquestrar as tasks.'''

    def run(self):
        # =====================================================================
        # ======================== LANDING ====================================

        extrator_alunos_landing = ExtracaoDadosBubbleAliunoMentor()
        extrator_alunos_landing.executar()

        extrator_db_landing = ExtracaoDadosBubbleDiarioBordo()
        extrator_db_landing.executar()

        extrator_metas_landing = ExtracaoApiNewGate()
        extrator_metas_landing.executar()

        # =====================================================================
        # ======================== TRUSTED ====================================

        manipulador_trusted_db_bubble = ManipulationTrustedDbBubble()
        manipulador_trusted_db_bubble.executar()

        manipulador_trusted_metas_newgate = ManipulationTrustedMetasNewgate()
        manipulador_trusted_metas_newgate.executar()

        manipulador_trusted_user_bubble = ManipulationTrustedUserBubble()
        manipulador_trusted_user_bubble.executar()

        # =====================================================================
        # ======================== BUSINESS ====================================

        apply_rule_rt = BusinessApplyRuleRT()
        apply_rule_rt.executar()


if __name__ == "__main__":
    main = Main()
    main.run()