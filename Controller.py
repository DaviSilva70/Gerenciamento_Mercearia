
from Models import Categoria, Estoque, Produtos, Fornecedor,Pessoa, Funcionario,Venda
from DAO import DaoCategoria,DaoEstoque,DaoFornecedor,DaoFuncionario,DaoPessoa,DaoVenda
from datetime import datetime

class ControllerCategoria():
    def Cadastra_Categoria(self,Nova_Categoria):
        categoria_existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == Nova_Categoria:
                categoria_existe = True
        if not categoria_existe:
            DaoCategoria.salvar(Nova_Categoria)
            print('Categoria Cadastrada com Sucesso.')
        else:
            print('A Categoria Que Deseja Cadastrar Ja Existe.')
    def Remover_Categoria(self,Remover_Categoria):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x:x.categoria == Remover_Categoria,x))
        if len(cat) <= 0:
            print('A Categoria que Deseja Remover Nao Existe.')
        else:
            for i in range(len(x)):
                    if x[i].categoria == Remover_Categoria:
                        del x[i]
                        break
            print('Categoria Removida com Sucesso.')
            #TODO: COLOCAR SEM CATEGORIA NO ESTOQUE
            with open('categoria.txt','w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')
    def Alterar_Categoris(self,Alterar_Categoria,Categoria_Alterada):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == Alterar_Categoria,x))
        if len(cat) > 0:
            cat_1 = list(filter(lambda x: x.categoria == Categoria_Alterada,x))
            if len(cat_1) == 0:
                x = list(map(lambda x: Categoria(Categoria_Alterada) if(x.categoria == Alterar_Categoria) else(x),x))
                print('Alteraçao Feita com Sucesso.')
            #TODO: ALTERAR A CATEGORIA TAMBEM DO ESTOQUE.    
            else:
                print('A Categoria Que Deseja Alterar Ja Existe.')    
        else:
            print('A Categoria que Deseja Alterar Nao Existe.')
        with open('categoria.txt','w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')        
    def Mostrar_Categoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Categoria Vazia.')
        else:
            for i in categorias:
                print('Categoria: {}.'.format(i.categoria))    

class ControllerEstoque():
    def Cadastrar_Produto(self,nome,preco,categoria,quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto Cadastrado com Sucesso..')
            else:
                print('Produto Ja Existe em Estoque.')
        else:
            print('Categoria Inexistente!')            
    
    def Remover_Produto(self,nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome,x))
        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
        else:
            print('O Produto que Desaja Remover Nao Existe.')
        with open('estoque.txt','w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + ' | ' + i.produto.preco + ' | ' + i.produto.categoria + ' | ' + str(i.quantidade))
                arq.writelines('\n')            
    
    def Alterar_Produto(self,Nome_Alterado,Novo_Nome,Novo_Preco,Nova_Categoria,Nova_Qquantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == Nova_Categoria,y))
        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == Nome_Alterado,x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == Novo_Nome,x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(Novo_Nome, Novo_Preco, Nova_Categoria),Nova_Qquantidade)if(x.produto.nome == Nome_Alterado)else(x),x))
                    print('Produto Alterado com Sucesso.')
                else:
                    print('Produto Ja Cadastrado.')    
            else:
                print('O Produto que Desaja Alterar Nao Existe.')
            with open('estoque.txt','w')as arq:
                for i in x:
                    arq.writelines(i.produto.nome + ' | ' + i.produto.preco + ' | ' + i.produto.categoria + ' | ' + str(i.quantidade))
                    arq.writelines('\n')       
        else:
            print('A Categoria Alterada Nao Existe.')
    def Mostrar_Estoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Estoque Vazio.')
        else:
            print('------------Produtos-----------')
            for i in estoque:
                print(f'Nome: {i.produto.nome}\n'
                      f'Preco: {i.produto.preco}\n'
                      f'Categoria: {i.produto.categoria}\n'
                      f'Quantidade: {i.quantidade}\n')
                print('-'*30)
 
class ControllerVenda():
    def Cadastrar_Venda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        produto_existe = False # Se existe Produto no Estoque.
        quantidade_existe = False # Nao tem quantidade suficinte em estoque.
        for i in x:
            if produto_existe == False:
                if i.produto.nome == nomeProduto:
                    produto_existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade_existe = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valorCompra = int(quantidadeVendida) * float(i.produto.preco)

                        DaoVenda.salvar(vendido)

            temp.append(Estoque(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade))

        arq = open('estoque.txt', 'w')
        arq.write("")


        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" + i.produto.categoria + "|" + int(i.quantidade))
                arq.writelines('\n')

        if produto_existe == False:
            print('Produto Nao Exite')
            return None
        elif not quantidade_existe:
            print('A Quantidade Vendida Nao Contem em Estoque')
            return None
        else:
            print("Produto Vendido Corretamente.")
            return valorCompra

    def Relatorio_Produtos(self):
        vendas = DaoVenda.ler()
        produtos = []
        for i in vendas:
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho)>0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
                if (x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': int(quantidade)})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esses são os produtos mais vendidos')
        a = 1
        for i in ordenado:
            print(f"==========Produto [{a}]==========")
            print(f"Produto: {i['produto']}\n"
                  f"Quantidade: {i['quantidade']}\n")
            a += 1
            
a = ControllerEstoque()
a.Cadastrar_Produto('Porco 6kg','5.00','Congelados',5)


"""a = ControllerCategoria()
a.Alterar_Categoris('Frios','Congelados')"""

"""a = ControllerEstoque()
a.Alterar_Produto('Asa','Contra-Asa','1.99','Congelados',320)"""

"""a = ControllerCategoria()
a.Mostrar_Categoria()"""

"""a = ControllerCategoria()
a.Cadastra_Categoria('Congelados')"""

"""a = ControllerEstoque()
a.Remover_Produto('Figado')"""

"""a = ControllerEstoque()
a.Mostrar_Estoque()"""

"""a = ControllerVenda()
a.Cadastrar_Venda('Frango 12kg','Isa','Ana',1500)"""

"""a = ControllerVenda()
a.Relatoria_Produtos()"""
# 1.14
