use mysql::*;
use mysql::prelude::*;
use std::ffi::CStr;
use std::os::raw::c_char;

/// 📌 Función para probar la conexión con MySQL
#[unsafe(no_mangle)]
pub extern "C" fn test_mysql_connection(
    host: *const c_char,
    port: u16,
    user: *const c_char,
    password: *const c_char,
    database: *const c_char,
) -> i32 {
    // Verificar que ningún puntero sea nulo
    if host.is_null() || user.is_null() || password.is_null() || database.is_null() {
        eprintln!("❌ Error: uno o más parámetros de conexión son nulos.");
        return 0;
    }

    // Convertir los punteros a cadenas Rust
    let host_str = unsafe { CStr::from_ptr(host) }.to_str().unwrap_or("");
    let user_str = unsafe { CStr::from_ptr(user) }.to_str().unwrap_or("");
    let password_str = unsafe { CStr::from_ptr(password) }.to_str().unwrap_or("");
    let database_str = unsafe { CStr::from_ptr(database) }.to_str().unwrap_or("");

    // Crear las opciones de conexión con OptsBuilder
    let opts = OptsBuilder::new()
        .ip_or_hostname(Some(host_str))
        .tcp_port(port)
        .user(Some(user_str))
        .pass(Some(password_str))
        .db_name(Some(database_str));

    // Intentar conectarse a la base de datos
    let pool = match Pool::new(opts) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("❌ Error al crear el pool de conexión: {:?}", e);
            return 0;
        }
    };

    let mut conn = match pool.get_conn() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("❌ Error al obtener la conexión: {:?}", e);
            return 0;
        }
    };

    // Ejecutar una consulta simple
    match conn.query_drop("SELECT 1") {
        Ok(_) => {
            println!("✅ Conexión exitosa a MySQL.");
            1 // Conexión exitosa
        }
        Err(e) => {
            eprintln!("❌ Error en la consulta de prueba: {:?}", e);
            0 // Error en la conexión
        }
    }
}

/// 📌 Función para insertar datos en la base de datos MySQL
#[unsafe(no_mangle)]
pub extern "C" fn insert_into_mysql(
    host: *const c_char,
    port: u16,
    user: *const c_char,
    password: *const c_char,
    database: *const c_char,
    data: *const c_char,
) -> i32 {
    // Verificar que ningún puntero sea nulo
    if host.is_null() || user.is_null() || password.is_null() || database.is_null() || data.is_null() {
        eprintln!("❌ Error: uno o más parámetros son nulos.");
        return 0;
    }

    // Convertir los punteros a cadenas Rust
    let host_str = unsafe { CStr::from_ptr(host) }.to_str().unwrap_or("");
    let user_str = unsafe { CStr::from_ptr(user) }.to_str().unwrap_or("");
    let password_str = unsafe { CStr::from_ptr(password) }.to_str().unwrap_or("");
    let database_str = unsafe { CStr::from_ptr(database) }.to_str().unwrap_or("");
    let data_str = unsafe { CStr::from_ptr(data) }.to_str().unwrap_or("");

    // Crear las opciones de conexión con OptsBuilder
    let opts = OptsBuilder::new()
        .ip_or_hostname(Some(host_str))
        .tcp_port(port)
        .user(Some(user_str))
        .pass(Some(password_str))
        .db_name(Some(database_str));

    // Intentar conectarse a la base de datos
    let pool = match Pool::new(opts) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("❌ Error al crear el pool de conexión: {:?}", e);
            return 0;
        }
    };

    let mut conn = match pool.get_conn() {
        Ok(c) => c,
        Err(e) => {
            eprintln!("❌ Error al obtener la conexión: {:?}", e);
            return 0;
        }
    };

    // Insertar el dato en la tabla "Entradas"
    match conn.exec_drop(
        "INSERT INTO Entradas (data) VALUES (:data)",
        params! { "data" => data_str },
    ) {
        Ok(_) => {
            println!("✅ Inserción exitosa en la base de datos.");
            1
        }
        Err(e) => {
            eprintln!("❌ Error al insertar en la base de datos: {:?}", e);
            0
        }
    }
}
