import { Root } from "./Root";
import { useComponent } from "widgetsjs";
import { Card } from "./Card";
import { Button } from "./Button";
import { Content } from "./Content";
useComponent(Root).as('x-root')
useComponent(Card).as('x-card')
useComponent(Content).as('x-content')
useComponent(Button).as('x-next')