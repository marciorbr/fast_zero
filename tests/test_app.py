"""
Fase 1 - Organizar (Arrange)
Nesta primeira etapa, estamos preparando o ambiente para o teste. No exemplo, a linha com o comentário Arrange não é o teste em si, ela monta o ambiente para que o teste possa ser executado. Estamos configurando um client de testes para fazer a requisição ao app.

Fase 2 - Agir (Act)
Aqui é a etapa onde acontece a ação principal do teste, que consiste em chamar o Sistema Sob Teste (SUT). No nosso caso, o SUT é a rota /, e a ação é representada pela linha response = client.get('/'). Estamos exercitando a rota e armazenando sua resposta na variável response. É a fase em que o código de testes executa o código de produção que está sendo testado. Agir aqui significa interagir diretamente com a parte do sistema que queremos avaliar, para ver como ela se comporta.

Fase 3 - Afirmar (Assert)
Esta é a etapa de verificar se tudo correu como esperado. É fácil notar onde estamos fazendo a verificação, pois essa linha sempre tem a palavra reservada assert. A verificação é booleana, ou está correta ou não está. Por isso, um teste deve sempre incluir um assert para verificar se o comportamento esperado está correto.
"""


def test_root_deve_retornar_200_e_ola_mundo(client):

    response = client.get('/')   # Act

    assert response.status_code == 200   # Assert
    assert response.json() == {'message': 'Olá Mundo!'}   # Assert


# def test_create_user(client):

#     response = client.post(
#         '/users/',
#         json={
#             'username': 'alice',
#             'email': 'alice@example.com',
#             'password': 'secret',
#         },
#     )
#     assert response.status_code == 201
#     assert response.json() == {
#         'username': 'alice',
#         'email': 'alice@example.com',
#         'id': 1,
#     }


# def test_read_users(client):
#     response = client.get('/users/')
#     assert response.status_code == 200
#     assert response.json() == {
#         'users': [
#             {
#                 'username': 'alice',
#                 'email': 'alice@example.com',
#                 'id': 1,
#             }
#         ]
#     }


# def test_update_user(client):
#     response = client.put(
#         '/users/1',
#         json={
#             'username': 'bob',
#             'email': 'bob@example.com',
#             'password': 'mynewpassword',
#         },
#     )

#     assert response.status_code == 200
#     assert response.json() == {
#         'username': 'bob',
#         'email': 'bob@example.com',
#         'id': 1,
#     }


# def test_delete_user(client):
#     response = client.delete(
#         '/users/1',
#     )

#     assert response.status_code == 200
#     assert response.json() == {'detail': 'User deleted'}
