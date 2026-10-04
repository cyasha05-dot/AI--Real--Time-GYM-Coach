import time
import streamlit as st


class VoicePipeline:

    def __init__(self, llm, tts):

        self.llm = llm
        self.tts = tts

        # Last time AI coach spoke
        self.last_spoken_at = 0

        # Voice cooldown
        self.cooldown = 5

    # ---------------------------------------------------------
    # FIND FORM ISSUE
    # ---------------------------------------------------------

    def _find_form_issue(self, exercise, metrics):

        if not metrics:
            return None

        # Direct issue from system
        if "issue" in metrics:
            return metrics["issue"]

        # -----------------------------------------------------
        # SQUATS
        # -----------------------------------------------------

        if exercise == "Squats":

            depth = metrics.get(
                "depth_status",
                ""
            )

            back_angle = metrics.get(
                "back_angle",
                180
            )

            if depth == "TOO HIGH":

                return (
                    "Your squat is too shallow. "
                    "Go deeper."
                )

            if isinstance(back_angle, (int, float)):

                if back_angle < 130:

                    return (
                        "You are leaning too far forward. "
                        "Keep your back straight."
                    )

        # -----------------------------------------------------
        # PUSH UPS
        # -----------------------------------------------------

        elif exercise == "Push-ups":

            alignment = metrics.get(
                "body_alignment",
                ""
            )

            hip_status = metrics.get(
                "hip_status",
                ""
            )

            if alignment == "Poor Form":

                return (
                    "Keep your body straight during "
                    "the push-up."
                )

            if hip_status == "SAGGING":

                return (
                    "Your hips are sagging. "
                    "Keep your body straight."
                )

            if hip_status == "PIKED UP":

                return (
                    "Your hips are too high. "
                    "Lower them."
                )

        # -----------------------------------------------------
        # BICEPS CURL
        # -----------------------------------------------------

        elif exercise == "Biceps Curls (Dumbbell)":

            swing = metrics.get(
                "swing_status",
                ""
            )

            shoulder = metrics.get(
                "shoulder_status",
                ""
            )

            if swing == "SWINGING":

                return (
                    "Stop swinging your body. "
                    "Keep the movement controlled."
                )

            if shoulder == "ELBOW DRIFTING":

                return (
                    "Keep your elbows close to "
                    "your body."
                )

        # -----------------------------------------------------
        # SHOULDER PRESS
        # -----------------------------------------------------

        elif exercise == "Shoulder Press":

            back_arch = metrics.get(
                "back_arch_status",
                ""
            )

            if back_arch == "Excessive Arch":

                return (
                    "Do not overarch your back. "
                    "Brace your core."
                )

            if back_arch == "Slight Arch":

                return (
                    "Brace your core and reduce "
                    "your back arch."
                )

        # -----------------------------------------------------
        # LUNGES
        # -----------------------------------------------------

        elif exercise == "Lunges":

            balance = metrics.get(
                "balance_status",
                ""
            )

            if balance == "OFF BALANCE":

                return (
                    "Keep your balance and maintain "
                    "a stable stance."
                )

        return None

    # ---------------------------------------------------------
    # PROCESS EVENT
    # ---------------------------------------------------------

    def process_event(
        self,
        event,
        exercise,
        metrics
    ):

        try:

            issue = self._find_form_issue(
                exercise,
                metrics
            )

            now = time.time()

            # Events that should always generate feedback
            major_events = [
                "workout_started",
                "set_completed",
                "workout_completed"
            ]

            # -------------------------------------------------
            # NORMAL FORM CHECK
            # -------------------------------------------------

            if event not in major_events:

                # No problem detected
                if not issue:
                    return None

                # Prevent speaking every frame
                if now - self.last_spoken_at < self.cooldown:
                    return None

            # -------------------------------------------------
            # ASK GROQ
            # -------------------------------------------------

            text = self.llm.give_feedback(
                event,
                issue
            )

            if not text:
                return None

            # -------------------------------------------------
            # TEXT TO SPEECH
            # -------------------------------------------------

            voice = self.tts.speak(text)

            if not voice:
                # Keep text feedback even if TTS fails
                self.last_spoken_at = now

                return (
                    None,
                    text
                )

            self.last_spoken_at = now

            return (
                voice,
                text
            )

        except Exception as e:

            print(
                f"Voice Pipeline Error: {e}"
            )

            return None


# -------------------------------------------------------------
# STREAMLIT AUDIO
# -------------------------------------------------------------

def autoplay_audio(audio_bytes):

    if not audio_bytes:
        return

    st.audio(
        audio_bytes,
        format="audio/mp3",
        autoplay=True
    )