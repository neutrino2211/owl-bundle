import { StatelessWidget } from "widgetsjs";

export class Root extends StatelessWidget {
    constructor(){
        super({})
    }

    render(state){
        return this.widgetChildren;
    }
}
