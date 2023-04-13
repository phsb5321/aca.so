## Entidades:

- Pessoa
    - Id
    - Nome

- Livro
    - Id
    - Nome
    - ISBN
    - Quantidade em estoque

Uma pessoa pode ser autor e/ou leitor de livros.

Um livro é sempre escrito por um ou mais autores.

Um autor pode ter vários livros.

Um leitor pode marcar livros como lidos, bem como avaliá-los com uma nota de 1 a 5 (valores inteiros) e um comentário de no máximo 256 caracteres.

Existe um estoque de livros, que pode ou não conter os livros.

## O que esperamos de rotas:

- CRUD de pessoa.
- CRUD de livros.
  - Nos endpoints de leitura (pegar um livro/listar livros) deve ser retornado os autores do livro, a nota de avaliação dele e quantas avaliações possui.
  - Na listagem de livros deve ser possível filtrar por apenas livros que estão no estoque ou por apenas os que não estão.
- Uma rota para listar livros de um autor.
- Uma rota para listar leitores de um livro.
  - Junto de cada leitor deve ser retornado também a nota e o comentário que ele atribuiu ao livro.
- Uma rota para listar os comentários de avaliação de um livro.

**Todas as rotas de listagem devem ter paginação**

## O que vamos avaliar:

- Design API
- Modelagem das entidades e relações
- Validações
- Arquitetura
- Interface com o banco de grafo

## Como rodar o servidor gremlin

Basta ter instalado o docker compose e executar o seguinte comando:

```sh
docker-compose up graph-db
```

## Como utilizar o GraphDB e pegar uma traversal (g)

Basta inicializar a classe:

```python
db = GraphDB()
g = db.get_traversal()
```


## Test Coverage

| Name                                                          | Stmts | Miss | Cover |
| ------------------------------------------------------------- | ----- | ---- | ----- |
| app/__init__.py                                               | 0     | 0    | 100%  |
| app/database/__init__.py                                      | 0     | 0    | 100%  |
| app/database/gremlin.py                                       | 28    | 0    | 100%  |
| app/database/models.py                                        | 55    | 0    | 100%  |
| app/routes/__init__.py                                        | 0     | 0    | 100%  |
| app/routes/authors_routes.py                                  | 22    | 22   | 0%    |
| app/routes/books_routes.py                                    | 47    | 47   | 0%    |
| app/routes/people_routes.py                                   | 42    | 42   | 0%    |
| app/routes/readers_routes.py                                  | 37    | 37   | 0%    |
| app/services/__init__.py                                      | 17    | 0    | 100%  |
| app/services/authors_services/__init__.py                     | 0     | 0    | 100%  |
| app/services/authors_services/create_authorship_service.py    | 23    | 4    | 83%   |
| app/services/authors_services/list_books_by_author_service.py | 23    | 2    | 91%   |
| app/services/books_services/__init__.py                       | 0     | 0    | 100%  |
| app/services/books_services/create_book_service.py            | 24    | 0    | 100%  |
| app/services/books_services/delete_book_service.py            | 17    | 2    | 88%   |
| app/services/books_services/get_book_by_id_service.py         | 26    | 0    | 100%  |
| app/services/books_services/list_books_service.py             | 36    | 0    | 100%  |
| app/services/books_services/update_book_service.py            | 21    | 2    | 90%   |
| app/services/people_services/__init__.py                      | 0     | 0    | 100%  |
| app/services/people_services/create_person_service.py         | 24    | 0    | 100%  |
| app/services/people_services/delete_person_service.py         | 19    | 2    | 89%   |
| app/services/people_services/get_person_by_id_service.py      | 19    | 1    | 95%   |
| app/services/people_services/list_people_service.py           | 21    | 0    | 100%  |
| app/services/people_services/update_person_service.py         | 23    | 2    | 91%   |
| app/services/readers_services/__init__.py                     | 0     | 0    | 100%  |
| app/services/readers_services/create_rating_service.py        | 35    | 6    | 83%   |
| app/services/readers_services/create_read_service.py          | 26    | 4    | 85%   |
| app/services/readers_services/list_ratings_by_book_service.py | 30    | 1    | 97%   |
| app/services/readers_services/list_readers_by_book_service.py | 21    | 1    | 95%   |
| TOTAL                                                         | 636   | 175  | 72%   |
