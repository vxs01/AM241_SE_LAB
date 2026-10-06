def check_catch(hook, fish_list):
    for fish in fish_list:
        if hook.get_rect().colliderect(fish.get_rect()):
            return fish
    return None