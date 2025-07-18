
# 1. Clases y relaciones

## 1. Producto
### Atributos
- `string nombre`
- `string codigo` // único
- `double precio`
- `int stock`
### Métodos
- `void actualizarStock(int cantidad)` // suma o resta
- `double valorTotal()` // `precio * stock`
- `string getInfo()` // imprime todos sus datos

---
# 2. Venta

### Atributos
- `string idVenta`
- `vector <pair<Producto*,int>> items`  // puntero al producto + cantidad vendida
- `double total`
### Métodos
- `void agregarItem(Producto* p, int cantidad)`
- `void procesar()` // descuenta stock y calcula `total`
- `double getTotal() const`