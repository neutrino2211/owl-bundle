import { StatelessWidget, useComponent } from "widgetsjs";

class Loader extends StatelessWidget {
    constructor(){
        super({})
    }

    render(){
        return `
            <div class="loader">
            </div>
        `
    }
}

useComponent(Loader).as('x-loader')