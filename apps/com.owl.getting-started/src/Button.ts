import { StatefulWidget } from "widgetsjs";

export class Button extends StatefulWidget {
    constructor(){
        super({
            disabled: true
        },{
            disabled: e=>e === true || e == 'true'
        })
    }

    onMount(){
        const btn = this.$child<HTMLButtonElement>('button');
        btn.addEventListener('click', () => {
            window.open('http://localhost:10000/Applications/com.owl.home/index.html', '_self')
        })
    }

    afterRender(){
        this.$child<HTMLButtonElement>('button').disabled = this.state.disabled;
    }

    render(state){
        console.log(state)
        return `<button class="${state.disabled ? 'inactive': 'active'}">${this.widgetChildren}</button>`;
    }
}