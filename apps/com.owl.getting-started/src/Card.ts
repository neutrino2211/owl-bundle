import { StatelessWidget } from "widgetsjs";

export class Card extends StatelessWidget {
    constructor(){
        super({})
    }

    render(){
        return `
        <div class="card">
            ${this.widgetChildren}
        </div>
        `
    }
}