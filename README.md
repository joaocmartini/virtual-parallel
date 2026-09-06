# Virtual Parallel

Virtual Parallel é uma integração personalizada para o Home Assistant que permite criar circuitos paralelos virtuais entre entidades `switch`.

As entidades adicionadas ao mesmo circuito são sincronizadas automaticamente. Quando uma delas é ligada ou desligada, as demais entidades disponíveis do circuito acompanham o mesmo estado.

## Recursos

- Circuitos paralelos virtuais entre entidades `switch`
- Sincronização bidirecional
- Qualquer entidade do circuito pode alterar o estado das demais
- Definição de uma entidade mestre
- Configuração pela interface do Home Assistant
- Edição dos circuitos existentes
- Ignora entidades `unknown` e `unavailable`
- Evita comandos desnecessários quando o estado já está correto

## Como funciona

Exemplo com três interruptores:

    switch.luz_sala
    switch.luz_corredor
    switch.luz_parede

Ao criar um circuito com essas entidades, o estado é sincronizado entre elas.

Se uma entidade for ligada:

    ON → as demais ficam ON

Se uma entidade for desligada:

    OFF → as demais ficam OFF

A sincronização funciona nos dois sentidos, permitindo que qualquer entidade disponível do circuito seja utilizada para controlar as demais.

## Instalação

A maneira recomendada de instalar o Virtual Parallel é através do HACS.

No Home Assistant:

1. Abra HACS.
2. Entre em Integrações.
3. Procure por Virtual Parallel.
4. Clique em Download.
5. Reinicie o Home Assistant.

Depois da instalação, acesse:

Configurações → Dispositivos e serviços → Adicionar integração

e procure por Virtual Parallel.

## Configuração

Ao adicionar a integração, informe o nome do circuito, selecione as entidades `switch` que participarão dele e escolha a entidade mestre.

Os circuitos podem ser editados posteriormente para alterar o nome, as entidades participantes ou a entidade mestre.

## Tratamento de indisponibilidade

Entidades nos estados `unknown` ou `unavailable` são ignoradas durante a sincronização.

Isso evita que uma entidade temporariamente indisponível seja interpretada como desligada e altere o estado das demais.

## Requisitos

- Home Assistant
- Entidades do domínio `switch`

## Versão

0.0.3

## Repositório

https://github.com/joaocmartini/virtual-parallel
