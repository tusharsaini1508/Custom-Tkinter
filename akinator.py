import customtkinter as ctk

class AkinatorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator Game")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")  
        self.question_label = ctk.CTkLabel(root, text="Think of an animal...", font=("Arial", 16), wraplength=500)
        self.question_label.pack(pady=20)
        self.button_frame = ctk.CTkFrame(root)
        self.button_frame.pack(pady=20)
        self.yes_button = ctk.CTkButton(self.button_frame, text="Yes", font=("Arial", 14), command=self.yes_pressed)
        self.yes_button.grid(row=0, column=0, padx=20)
        self.no_button = ctk.CTkButton(self.button_frame, text="No", font=("Arial", 14), command=self.no_pressed)
        self.no_button.grid(row=0, column=1, padx=20)
        self.restart_button = ctk.CTkButton(root, text="Restart", font=("Arial", 14), command=self.restart_game)
        self.restart_button.pack(pady=20)
        self.restart_button.pack_forget()
        self.game_tree = {
            "Is it a mammal?": {
                "yes": {
                    "Is it domesticated?": {
                        "yes": {
                            "Does it bark?": {
                                "yes": "Is it a dog?",
                                "no": {
                                    "Does it purr?": {
                                        "yes": "Is it a cat?",
                                        "no": "Is it a cow?"
                                    }
                                }
                            }
                        },
                        "no": {
                            "Is it a wild cat?": {
                                "yes": {
                                    "Does it have a mane?": {
                                        "yes": "Is it a lion?",
                                        "no": "Is it a tiger?"
                                    }
                                },
                                "no": {
                                    "Is it the largest land animal?": {
                                        "yes": "Is it an elephant?",
                                        "no": {
                                            "Does it have a horn?": {
                                                "yes": "Is it a rhino?",
                                                "no": "Is it a deer?"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "no": {
                    "Does it live in water?": {
                        "yes": {
                            "Is it a mammal?": {
                                "yes": "Is it a dolphin?",
                                "no": {
                                    "Does it have scales?": {
                                        "yes": "Is it a fish?",
                                        "no": {
                                            "Does it have tentacles?": {
                                                "yes": "Is it an octopus?",
                                                "no": "Is it a jellyfish?"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "no": {
                            "Does it fly?": {
                                "yes": {
                                    "Is it a bird of prey?": {
                                        "yes": "Is it an eagle?",
                                        "no": {
                                            "Does it have colorful feathers?": {
                                                "yes": "Is it a parrot?",
                                                "no": "Is it a pigeon?"
                                            }
                                        }
                                    }
                                },
                                "no": {
                                    "Does it have legs?": {
                                        "yes": {
                                            "Is it a reptile?": {
                                                "yes": "Is it a lizard?",
                                                "no": {
                                                    "Does it hop?": {
                                                        "yes": "Is it a frog?",
                                                        "no": "Is it a snake?"
                                                    }
                                                }
                                            }
                                        },
                                        "no": {
                                            "Is it an invertebrate?": {
                                                "yes": {
                                                    "Does it spin a web?": {
                                                        "yes": "Is it a spider?",
                                                        "no": "Is it a worm?"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        self.current_question = self.game_tree

    def yes_pressed(self):
        self.next_question("yes")

    def no_pressed(self):
        self.next_question("no")

    def next_question(self, answer):
        next_step = self.current_question.get(list(self.current_question.keys())[0]).get(answer)
        if isinstance(next_step, dict):
            self.current_question = next_step
            self.question_label.configure(text=list(self.current_question.keys())[0])
        else:
            self.question_label.configure(text=next_step)
            self.yes_button.configure(state=ctk.DISABLED)
            self.no_button.configure(state=ctk.DISABLED)
            self.restart_button.pack()

    def restart_game(self):
        self.current_question = self.game_tree
        self.question_label.configure(text=list(self.current_question.keys())[0])
        self.yes_button.configure(state=ctk.NORMAL)
        self.no_button.configure(state=ctk.NORMAL)
        self.restart_button.pack_forget()

if __name__ == "__main__":
    root = ctk.CTk()
    game = AkinatorGame(root)
    root.mainloop()
