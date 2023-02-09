#[macro_use] extern crate rocket;

mod login;


#[get("/")]
fn index() -> &'static str {
    "<h1>Hello, world!</h1>"
}

/* 
#[get("/login")]
pub fn login() -> &'static str {
    "This should be a login window :("
}
*/
#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index, login::login])       
}