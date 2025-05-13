# dfs-python-bindings
Python bindings for [Distributional Formal Semantics (DFS)](https://github.com/hbrouwer/dfs-tools) tools

```
>>> import dfs_python_bindings as dpb
>>> dpb.dfs_load_world("../dfs-tools/worlds/wollic2019.pl")
%%%% DFS Tools 0.2.1 | https://github.com/hbrouwer/dfs-tools

>>> models = dpb.dfs_sample_models(10)
[...]
>>> mspace = dpb.dfs_models_to_numpy(models)
>>> mspace
{'ask_menu(ellen)': array([0, 0, 1, 0, 0, 0, 0, 1, 0, 1]), 'ask_menu(john)': array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0]), 'leave(ellen)': array([0, 0, 0, 1, 0, 0, 0, 0, 1, 0]), 'leave(john)': array([1, 1, 0, 0, 0, 0, 0, 0, 0, 1]), 'pay(ellen)': array([0, 0, 1, 0, 1, 1, 0, 1, 1, 0]), 'pay(john)': array([1, 1, 0, 1, 1, 0, 0, 1, 0, 1]), 'drink(ellen,beer)': array([1, 0, 0, 0, 0, 0, 0, 0, 1, 1]), 'drink(ellen,wine)': array([1, 1, 1, 0, 0, 1, 1, 1, 0, 0]), 'drink(john,beer)': array([1, 0, 1, 0, 0, 1, 0, 0, 1, 1]), 'drink(john,wine)': array([0, 0, 1, 0, 1, 1, 0, 0, 1, 0]), 'eat(ellen,fries)': array([0, 1, 1, 1, 0, 1, 1, 0, 1, 0]), 'eat(ellen,pizza)': array([0, 0, 0, 1, 0, 0, 1, 0, 1, 1]), 'eat(john,fries)': array([0, 1, 1, 1, 0, 1, 0, 0, 1, 1]), 'eat(john,pizza)': array([0, 0, 0, 0, 0, 0, 1, 1, 1, 0]), 'enter(ellen,bar)': array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0]), 'enter(ellen,restaurant)': array([1, 1, 1, 1, 0, 0, 0, 0, 1, 0]), 'enter(john,bar)': array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]), 'enter(john,restaurant)': array([0, 0, 1, 1, 0, 1, 1, 1, 1, 1]), 'order(ellen,beer)': array([1, 0, 0, 0, 0, 1, 0, 0, 1, 1]), 'order(ellen,fries)': array([0, 1, 1, 1, 0, 1, 1, 1, 1, 0]), 'order(ellen,pizza)': array([1, 1, 0, 1, 0, 0, 1, 0, 1, 1]), 'order(ellen,wine)': array([1, 1, 1, 1, 0, 1, 1, 1, 1, 1]), 'order(john,beer)': array([1, 1, 1, 1, 0, 1, 1, 1, 1, 1]), 'order(john,fries)': array([1, 1, 1, 1, 0, 1, 0, 0, 1, 1]), 'order(john,pizza)': array([0, 0, 1, 1, 0, 1, 1, 1, 1, 1]), 'order(john,wine)': array([0, 0, 1, 0, 1, 1, 0, 0, 1, 0])}
```
