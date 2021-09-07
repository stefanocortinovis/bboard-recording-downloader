from pathlib import Path


def validate(args):
    validated_args = dict()
    
    dest = Path(args.dest)
    if not dest.is_dir():
        raise FileNotFoundError(f"No such file or directory: {dest}")
    validated_args['dest'] = dest
    validated_args['url'] = input("Paste the recording URL: ") if args.url is None else args.url # TODO: validate as valid URL

    if (browser := args.browser.lower()) == 'chrome':
        validated_args['executable_path'] = './chromedriver' if args.executable_path == 'default' else args.executable_path
    elif browser == 'firefox':
        validated_args['executable_path'] = './geckodriver' if args.executable_path == 'default' else args.executable_path
    validated_args['browser'] = browser
    validated_args['headless'] = args.headless
    validated_args['T'] = args.T

    return validated_args
