const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            token: null,
            message: null,
            demo: [
                {
                    title: "FIRST",
                    background: "white",
                    initial: "white"
                },
                {
                    title: "SECOND",
                    background: "white",
                    initial: "white"
                }
            ]
        },
        actions: {
            exampleFunction: () => {
                getActions().changeColor(0, "green");
            },

            syncTokenFromSessionStore: () => {
                const token = sessionStorage.getItem("token");
                console.log("Application just loaded, syncing the session storage token");
                if (token && token !== "" && token !== undefined) setStore({ token: token });
            },

            logout: () => {
                sessionStorage.removeItem("token");
                console.log("Logout");
                setStore({ token: null });
            },

            login: async (email, password) => {
                const opts = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                    }),
                };

                try {
                    const resp = await fetch("https://3001-4geeksacade-crauthentic-xglz5fbliet.ws-us98.gitpod.io/api/token", opts);
                    if (resp.status !== 200) {
                        alert("There has been some error");
                        return false;
                    }

                    const data = await resp.json();
                    console.log("This came from the backend", data);
                    sessionStorage.setItem("token", data.access_token);
                    setStore({ token: data.access_token });
                    return true;
                } catch (error) {
                    console.error("There has been an error logging in", error);
                }
            },

            getMessage: async () => {
                const store = getStore();
                const opts = {
                    headers: {
                        Authorization: "Bearer " + store.token
                    }
                };
                try {
                    const resp = await fetch("https://3001-4geeksacade-crauthentic-xglz5fbliet.ws-us98.gitpod.io/api/hello", opts);
                    if (resp.status !== 200) {
                        console.log("Error loading message from backend");
                        return;
                    }
                    const data = await resp.json();
                    setStore({ message: data.message });
                } catch (error) {
                    console.log("Error loading message from backend", error);
                }
            },

            changeColor: (index, color) => {
                const store = getStore();
                const demo = store.demo.map((elm, i) => {
                    if (i === index) {
                        return {
                            ...elm,
                            background: color
                        };
                    } else {
                        return elm;
                    }
                });
                setStore({ demo: demo });
            }
        }
    };
};

export default getState;