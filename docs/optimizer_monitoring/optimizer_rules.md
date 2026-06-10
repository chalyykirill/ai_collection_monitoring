# Правила бизнес-оптимизатора

Событие `optimizer_mass_reject` означает массовый рост решений reject или
no action одновременно с падением `cnt_approved_for_communication`. Это не
является штатным режимом и классифицируется как `potential_incident`.

Возможные причины: изменение правил, исчерпание бюджета, некорректные входные
признаки или справочники коммуникаций. Все причины требуют проверки.

Основные метрики: `reject_share`, `cnt_approved_for_communication`,
`cnt_rejected_by_optimizer`, communication mix и
`unknown_communication_share`.

