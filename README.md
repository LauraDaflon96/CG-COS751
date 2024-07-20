# Ray Tracing

Este repositório contém uma implementação simples de ray tracing usando o modelo de iluminação Phong. O código gera uma imagem 2D com esferas iluminadas por uma fonte de luz, utilizando reflexões e sombreamento para criar efeitos realistas. A localização e tamanho das esferas é gerado aleatoriamente, mas existe a possibilidade de alterar o número máximo de esferas que deseja gerar.

### Pré-requisitos

- Python 3.x
- numpy
- matplotlib
- python-dotenv

### Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/LauraDaflon96/CG-COS751.git
    ```

2. Instale os pacotes necessários:

    ```bash
    pip install -r requirements
    ```

3. Crie um arquivo `.env` no diretório raiz com o seguinte conteúdo:

    ```dotenv
    NUM_SPHERES=5
    HEIGHT=800
    WIDTH=800
    ```

### Uso

1. Certifique-se de que as variáveis de ambiente necessárias estão definidas no seu arquivo `.env`.
2. Execute o script para gerar a imagem com ray tracing:

    ```bash
    python ray_tracing.py
    ```

3. A imagem gerada será salva como `image.png` no diretório raiz.

### Estrutura principal do código


#### Importações e Variáveis de Ambiente

```python
import numpy as np
import matplotlib.pyplot as plt
from ray_tracing import Ray
from vector_operations import VectorOperations
from dotenv import load_dotenv, dotenv_values
import os
import random

vals = dotenv_values("/caminho/para/seu/.env")

num_spheres = int(vals['NUM_SPHERES'])
width = int(vals['HEIGHT'])
height = int(vals['WIDTH'])
```

#### Inicialização dos Objetos

```python
objects = [
    {'type': 'sphere', 
     'center': np.array([0, -9000, 0]), 
     'radius': 9000 - 0.7, 
     'ambient': np.array([0.1, 0.1, 0.1]), 
     'diffuse': np.array([0.6, 0.6, 0.6]), 
     'specular': np.array([1, 1, 1]), 
     'shininess': 100, 
     'reflection': 0.5}
]

for sphere in range(0, num_spheres):
    objects.append(
        {'type': 'sphere', 
         'center': np.array([random.uniform(-0.3, 0.3), random.uniform(-0.5, 1.0), random.uniform(-1, 0.0)]), 
         'radius': random.uniform(0.0, 0.5), 
         'ambient': np.array([random.uniform(0.0, 0.1), random.uniform(0.0, 0.1), random.uniform(0.0, 0.1)]), 
         'diffuse': np.array([random.uniform(0.0, 0.9), random.uniform(0.0, 0.9), random.uniform(0.0, 0.9)]), 
         'specular': np.array([1, 1, 1]), 
         'shininess': 100, 
         'reflection': 0.5}
    )
```

#### Configuração da Câmera e Tela

```python
camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1/ratio, 1, -1/ratio)
image = np.zeros((height, width, 3))
max_depth = 3
light = {'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1]), 'diffuse': np.array([1, 1, 1]), 'specular': np.array([1, 1, 1])}
```

#### Loop de Renderização

```python
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        pixel = np.array([x, y, 0])
        ray = Ray(origin=camera, pixel=pixel)
        
        col = ray.colorize(np.array([0.2, 0.1, 0.7]))
        image[i][j] = col
        
        color = np.zeros((3))
        reflection = 1

        ray.nearest_intersected_object(objects)
        
        if ray.nearest_object is None:
            continue
        
        illumination = ray.illuminate(objects, light, camera)
        
        if np.any(illumination == None):
            image[i, j] = np.clip(0, 0, 0)
            continue
        
        color += reflection * illumination
        reflection = ray.reflection(illumination=illumination, reflection=reflection)
        image[i, j] = np.clip(color, 0, 1)

plt.imsave('image.png', image)
```

## Decisões Tomadas
O código foi dividido em diferentes módulos para melhorar a organização e facilitar a manutenção. Isso inclui separar as operações de vetores em `vector_operations.py` e a lógica principal de ray tracing em `ray_tracing.py`. Também foi utilizada a biblioteca dotenv para gerenciar as variáveis de ambiente, permitindo uma fácil configuração de parâmetros como o número de esferas e as dimensões da imagem. Quanto ao modelo de iluminação, foi escolhido o Phong por sua simplicidade e eficiência em produzir efeitos visuais realistas, incluindo componentes de iluminação ambiente, difusa e especular.


## Mudanças Futuras
Atualmente, o código só suporta esferas. Seria interessante adicionar suporte para outros tipos de objetos, como planos e triângulos, para aumentar a flexibilidade e as possibilidades de cenas. Há também a possibilidade de melhorar o modelo de iluminação adicionando efeitos de iluminação global, como reflexão difusa (ambient occlusion) e caustics, para obter uma renderização ainda mais realista. Por fim, as otimizações de desempenho serão necessárias à medida que o número de objetos e a complexidade das cenas aumentarem. Isso pode incluir paralelização do código e o uso de estruturas de dados mais eficientes para acelerar a busca de interseções.
