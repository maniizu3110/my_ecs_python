# セットアップ

## 前提条件

- python3(python)

## 構築方法

MacOS と Linux で手動で virtualenv を作成するには、以下のようにします。

```
python3 -m venv .venv
```

init プロセスが完了し、virtualenv が作成されたら、以下のように
を実行して、virtualenv を有効にします。

```
source .venv/bin/activate
```

virtualenv が有効化されたら、必要な依存関係をインストールします。

```
pip install -r requirements.txt
```

この時点で、このコードに対応した CloudFormation のテンプレートを合成することができます。

```
cdk synth
```

## Useful commands

- cdk ls` アプリ内のスタックを全てリストアップします。
- `cdk synth` 合成された CloudFormation のテンプレートを出力します。
- `cdk deploy` このスタックをデフォルトの AWS アカウント/リージョンにデプロイする
- cdk diff` デプロイされたスタックと現在の状態を比較する
- `cdk docs` CDK のドキュメントを開く

# 使用方法

- [] プロジェクト名の置き換え(default minbakoecs)
- [] ecr の作成
  - [] ecr のリポジトリの作成
- [] ドメインの取得
  1. **他サイトで登録済みの場合は、Route53 のネームサーバーを変更する**# my_ecs_python
