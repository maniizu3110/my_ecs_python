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

## TODO

- ドメイン取得
- backstage コンテナが動くようにする
- リファクタリング
  - 命名規則の整理
- redis
- メール
- codePipeline でのデプロイ（ヘルスチェックが通らなければ失敗とする）
- ヘルスチェックに使用する情報を.env から受け取る
- ドメインが決まった時に tls 対応
- ベーシック認証対応
- 通知設定
- アラート設定
- 各アプリケーション用のテンプレート用 Dockerfile の提供

## 長期 TODO

- next,react,laravel,go のスタートアッププロジェクトを作成するテンプレートの作成
  - eslint,prettier の設定,husky の設定,version の指定など
  - docker-compose の設定- ビルドが通るかの確認するための github actions の設定
  - セキュリティテストの自動化
  - インフラ定義に問題がないか
  - swagger の定義から、エンドポイントごとにテストを実行する
- ごく簡単な負荷テスト
  - swagger の定義から、エンドポイントごとにテストを実行する
