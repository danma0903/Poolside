import { useEffect } from "react";
import { AppState } from "react-native";
import EventSource from "react-native-sse";
import { EventSourceListener } from "react-native-sse";

type AlertEvent = "alert";
const es = new EventSource<AlertEvent>("myurlplaceholder");

const alertHandler: EventSourceListener<AlertEvent, "alert"> = (event) => {
	console.log("alert_received");
};

export default function AlertBox() {
	useEffect(() => {
		const appStateEventSub = AppState.addEventListener("change", (newState) => {
			if (newState === "active") {
				es.open();
				es.addEventListener("alert", alertHandler);
			} else if (newState === "background" || newState === "inactive") {
				es.removeAllEventListeners();
				es.close();
			}
		});
		return () => {
			appStateEventSub.remove();
		};
	});
	return <></>;
}
