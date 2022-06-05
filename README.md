# orbit-ia
![background-orbit-com-slogan](https://user-images.githubusercontent.com/56441318/171164559-775dfbf2-5a23-4b91-b0fb-6318a50cebac.png)

# Modelo CRISP-DM
O modelo CRISP-DM é uma metodologia que fornece uma abordagem estruturada para processos de mineração de dados, sendo amplamente utilizada devido à sua poderosa praticidade, flexibilidade e utilidade ao usar a análise e a valoração cíclica para resolver problemas complexos.

![diag](https://user-images.githubusercontent.com/29134051/163732347-33e290ba-d58b-42dc-8611-f4f3cf757ec8.jpg)

## Etapas do processo:

- [x] [Business Understanding](https://github.com/Orbit-API/orbit-docs#backlog-do-produto-resumido): 
Após o problema geral ser apresentado, foram realizados pesquisas e estudos sobre, além da elaboração de questionamentos para aprofundar o conhecimento da equipe sobre o que realmente atenderia a necessidade do cliente.

- [x] [Data Understanding](https://github.com/Orbit-API/orbit-ia/tree/main/analisys/data_understanding): 
Logo após o entendimento do negócio, foram iniciados os estudos sobre quais dados teriam maior valor para a construção do modelo. Também foram iniciadas pesquisas sobre ferramentas e tecnologias que pudessem ser úteis tanto para a coleta, quanto para o tratamento e armazenamento desses dados.

- [x] [Data Preparation](https://github.com/Orbit-API/orbit-ia/tree/main/analisys/data_preparation):
Com a estruturação do sistema de monitoramento concluída, foi possível captar dados provenientes da aplicação alvo, e armazená-los num banco de dados para uso futuro. Foi medida a correlação de registros de cada métrica escolhida, e os valores distoantes foram ajustados.

- [x] [Modeling](https://github.com/Orbit-API/orbit-ia/blob/main/api_ia_slack/orbit_ia.py):
Através de estudos das ferramentas disponíveis, escolhemos duas delas que melhor se alinharam com nosso método, para então estruturar o modelo da inteligência artificial: uma para realizar a previsão baseada em dados anteriores, e outra para auxiliar o sistema na tomada de decisão.

- [x] [Evaluation](https://github.com/Orbit-API/orbit-docs#projeto-em-funcionamento):
Realizamos testes com o modelo gerado para validar se atendem às necessidades do negócio.

- [x] [Deployment](https://github.com/Orbit-API/orbit-ia/tree/main/api_ia_slack):
A IA desenvolvida estará acessível como um serviço disponibilizado por uma aplicação Flask que periodicamente receberá dados coletados da aplicação alvo. De acordo com o resultado obtido à partir da análise realizada pelo modelo serão enviadas mensagens de alerta via Slack para notificar a equipe e auxiliar na tomada de decisão.
